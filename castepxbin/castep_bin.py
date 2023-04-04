"""
Reader module for CASTEP `castep_bin` files, a binary dump
file that can contain the parameters, cell, model, and results
(e.g., energies, forces, densities, wavefunctions) for a partciular
CASTEP run.

Reading this file can be beneficial as it uses the native floating-point
precision of the CASTEP run itself.

This implementation takes inspiration from similar functions in the
the [Euphonic](https://github.com/pace-neutrons/Euphonic) package.
"""

import io

# pylint: disable=invalid-name,too-few-public-methods
import re
from pathlib import Path
from struct import unpack
from typing import Any, Collection, Dict, List, Optional, Tuple, Union

import numpy as np

__all__ = ("read_castep_bin",)

TYPE_MAP = {
    int: "i4",
    float: "f8",
    complex: "c16",
}


class FieldType:
    """Abstract representation of the field type"""

    def __init__(self, name, dtype, endian="BIG"):
        self.name = name
        ed = ">" if endian.lower() == "big" else "<"
        dtype = TYPE_MAP.get(dtype, dtype)
        self.type_string = f"{ed}{dtype}"

    def decode(self, fp, decoded=None, record_data=None):
        """
        Decode the field with given file object or existing byte array
        """
        _ = decoded
        if record_data is None:
            record_data, marker = _read_record(fp)
        else:
            marker = len(record_data)
        count = marker // int(re.match(r"[><][a-z?]+(\d+)", self.type_string).group(1))
        return np.frombuffer(record_data, np.dtype(self.type_string), count=count)


class CompositeField:
    """Composition field - multiple entities are stored in a single record"""

    def __init__(self, fields: List[FieldType]) -> None:
        super().__init__()
        self.fields = fields


class ScalarField(FieldType):
    """Abstract Representation of sclar type"""

    def decode(self, fp, decoded=None, record_data=None):
        array = super().decode(fp, decoded, record_data)
        return array.tolist()[0]

    @property
    def shape(self):
        return (1,)


class SkippedField(FieldType):
    """A field that will be skipped"""

    def __init__(self):
        super().__init__("None", dtype="i4")

    def decode(self, fp, decoded=None, record_data=None):
        """Recode - read the field the advance the stream"""
        _read_record(fp)


class ArrayField(ScalarField):
    """Abstract Representation of a Array type"""

    def __init__(self, name, dtype, shape, endian="BIG"):
        """Instantiate an array field"""
        super().__init__(name, dtype, endian)
        self._shape = shape

    @property
    def shape(self):
        return self._shape

    def resolve_shape(self, data):
        """Resolve the shape of the array"""
        shape = []
        # Allow one dimension to be unresolved
        nunspec = 0
        missing = None
        for val in self.shape:
            if isinstance(val, str):
                missing = val
                val = data.get(val, -1)
                if val == -1:
                    nunspec += 1

            shape.append(val)
        if nunspec > 1:
            raise RuntimeError(f"Cannot resolve the shape: {shape}")

        return tuple(shape), missing

    def decode(self, fp, decoded=None, record_data=None):
        """
        Decode the array from the record

        Try to resolve single unresolved dimensions. The resolved size will be
        stored in the decoded data. Search of the data can be either from a
        the file object, or from an buffer that is already read. The latter
        case is needed so composite record can be supported....
        """
        if record_data is None:
            record_data, _ = _read_record(fp)
        if decoded is None:
            decoded = {}
        shape, missing_dim = self.resolve_shape(decoded)
        count = np.prod(shape)
        # Fully specified
        if count > 0:
            array = np.frombuffer(record_data, np.dtype(self.type_string), count=count)
        else:
            # Not fully specified - in this case we read the full record
            array = np.frombuffer(record_data, np.dtype(self.type_string), count=-1)
            # Work out the missing dimension...
            tot = array.size
            left = -tot / np.prod([elem for elem in shape if isinstance(elem, int)])
            decoded[missing_dim] = int(left)
            # Reconstruct the shape array
            actual_shape = []
            for elem in shape:
                if elem == -1:
                    actual_shape.append(int(left))
                else:
                    actual_shape.append(elem)
            shape = actual_shape

        # Special case for 1D string array - return a list of strings
        if "a" in self.type_string and len(self.shape) == 1:
            return [tmp.decode().strip() for tmp in array]
        array = np.reshape(array, shape, order="F")
        return array


class StrField(ScalarField):
    """Abstract Representation of a Array type"""

    def decode(self, fp, decoded=None, record_data=None):
        bdata = super().decode(fp, decoded, record_data)
        return bdata.decode().strip()


class BoolField(ScalarField):
    """
    A boolean field

    Note that LOGICAL type is typically represented as INTEGER by Fortran.
    Different compilers may have different conventions, but 0 can be consistently
    identified as .FALSE.
    """

    def __init__(self, name, endian="BIG"):
        super().__init__(name, "i4", endian)

    def decode(self, fp, decoded=None, record_data=None):
        val = super().decode(fp, decoded, record_data)
        return bool(val)  # Anything !=0 is True


class StructuredField:
    """A field that require case-by-case parsing"""

    def __init__(self, endian="BIG"):
        self.endian = endian
        self.endian_sym = ">" if endian.lower() == "big" else "<"


class EigenValueAndOccCompositeField(StructuredField):
    """Complex field for the eigenvalues and the occupations"""

    def decode(self, fp, decoded_data, record_data=None):
        """Decode the occupation and eigenvalues field"""
        _ = record_data
        nbands = decoded_data["nbands"]
        nspin = decoded_data["nspins"]
        nkpts = decoded_data["nkpts"]
        kpoints = np.zeros((3, nkpts))
        occ = np.zeros((nbands, nkpts, nspin))
        eigenvalues = np.zeros((nbands, nkpts, nspin))

        # Now start reading
        for ik in range(nkpts):
            data, _ = _read_record(fp)
            kpoints[:, ik] = np.frombuffer(data, self.endian_sym + "f8")
            for idx_spin in range(nspin):
                data, _ = _read_record(fp)
                occ[:, ik, idx_spin] = np.frombuffer(data, self.endian_sym + "f8")
                data, _ = _read_record(fp)
                eigenvalues[:, ik, idx_spin] = np.frombuffer(
                    data, self.endian_sym + "f8"
                )
        decoded_data["occupancies"] = occ
        decoded_data["eigenvalues"] = eigenvalues
        # Kpoints consistent with the order of eigenvalues and occupancies - as distribution of the
        # kpoints may result in a different order compared to those specified in the CELL part
        decoded_data["kpoints_of_eigenvalues"] = kpoints


class ChargeDensityField(StructuredField):
    """For reading charge density"""

    def decode(self, fp, decoded_data, record_data=None):
        """
        Decode the charge density
        """
        _ = record_data
        ngx_fine = decoded_data["ngx_fine"]
        ngy_fine = decoded_data["ngy_fine"]
        ngz_fine = decoded_data["ngz_fine"]
        nspin = decoded_data["nspins"]

        # Check if NCM
        has_ncm = decoded_data["spin_treatment"] == "VECTOR"

        charge_density = np.zeros((ngx_fine, ngy_fine, ngz_fine), dtype=complex)
        zcol = np.zeros(ngz_fine, dtype=complex)

        if nspin == 2 and not has_ncm:
            spin_density = np.zeros((ngx_fine, ngy_fine, ngz_fine), dtype=complex)

        if has_ncm:
            spin_density = np.zeros((ngx_fine, ngy_fine, ngz_fine, 3), dtype=complex)

        for _ in range(ngx_fine):
            for _ in range(ngy_fine):
                data, _ = _read_record(fp)
                nx = np.frombuffer(data, self.endian_sym + "i4", offset=0, count=1)[0]
                ny = np.frombuffer(data, self.endian_sym + "i4", offset=4, count=1)[0]
                zcol = np.frombuffer(
                    data, self.endian_sym + "c16", offset=8, count=ngz_fine
                )
                charge_density[nx - 1, ny - 1, :] = zcol
                # For NSPIN = 2
                if nspin == 2 and not has_ncm:
                    spin_col = np.frombuffer(
                        data,
                        self.endian_sym + "c16",
                        offset=8 + 16 * ngz_fine,
                        count=ngz_fine,
                    )
                    spin_density[nx - 1, ny - 1, :] = spin_col
                if has_ncm:
                    spin_col = np.frombuffer(
                        data,
                        self.endian_sym + "c16",
                        offset=8 + 16 * ngz_fine,
                        count=ngz_fine * 3,
                    )
                    spin_density[nx - 1, ny - 1, :, :] = spin_col.reshape(
                        (ngz_fine, 3), order="C"
                    )

        if nspin == 2 or has_ncm:
            decoded_data["spin_density"] = spin_density
        decoded_data["charge_density"] = charge_density


class WaveFunctionField(StructuredField):
    """For reading the wave function"""

    STORE_COEFFS = False

    @staticmethod
    def decode(fp, decoded_data, record_data=None):
        """
        Decode the charge density
        """
        _ = record_data
        ngx = decoded_data["ngx"]
        ngy = decoded_data["ngy"]
        ngz = decoded_data["ngz"]
        spinorcomps = decoded_data["wave_spinorcomps"]
        nbands_max = decoded_data["wave_nbands_max"]
        nkpts = decoded_data["wave_nkpts"]
        nspins = decoded_data["wave_nspins"]
        coeff_size_1 = decoded_data["wave_coeff_size_1"]

        # Main storage space for the coefficients
        coeffs = np.zeros(
            (coeff_size_1, spinorcomps, nbands_max, nkpts, nspins),
            order="F",
            dtype=complex,
        )

        nwaves_at_kp = np.zeros(nkpts, dtype=int)
        kpts = np.zeros((3, nkpts), dtype=float, order="F")
        pw_grid_coord = np.zeros((3, coeff_size_1, nkpts), dtype=int, order="F")

        record_spec1 = CompositeField(
            [ArrayField("kpt", dtype=float, shape=(3,)), ScalarField("nwaves", int)]
        )

        for ispin in range(nspins):
            for ik in range(nkpts):
                (  # pylint: disable=unbalanced-tuple-unpacking
                    kpts[:, ik],
                    nwaves,
                ) = _decode_composite(fp, record_spec1)
                nwaves_at_kp[ik] = nwaves
                wavecoords_spec = ArrayField("grid", int, (nwaves,))
                coeff_spec = ArrayField("coeff", complex, (nwaves,))
                # Read the coordinates of the plane waves with the unit of the reciprocal lattice vectors
                coords_x = wavecoords_spec.decode(fp)
                coords_y = wavecoords_spec.decode(fp)
                coords_z = wavecoords_spec.decode(fp)
                pw_grid_coord[0, :nwaves, ik] = coords_x
                pw_grid_coord[1, :nwaves, ik] = coords_y
                pw_grid_coord[2, :nwaves, ik] = coords_z
                for iband in range(nbands_max):
                    for ispinor in range(spinorcomps):
                        this_coeff = coeff_spec.decode(fp)
                        coeffs[:nwaves, ispinor, iband, ik, ispin] = this_coeff

        # Collect the data
        data = {
            "ngx": ngx,
            "ngy": ngy,
            "ngz": ngz,
            "pw_grid_coords": pw_grid_coord,
            "coeffs": coeffs,
            "kpts": kpts,
            "nwaves_at_kp": nwaves_at_kp,
            **{
                key.replace("wave_", ""): value
                for key, value in decoded_data.items()
                if key.startswith("wave_")
            },
        }
        # Save the data under the key 'wavefunction'
        decoded_data["wavefunction"] = data


# Defines the location of field relative to the tags
CASTEP_BIN_FIELD_SPEC = {
    # Parameters
    "BEGIN_ELECTRONIC": (
        SkippedField(),
        SkippedField(),
        SkippedField(),
        SkippedField(),  # nspin
        SkippedField(),  # nbands - no need to read again
        ScalarField("elec_temp", float),  # elect
        SkippedField(),
        SkippedField(),
        SkippedField(),
        StrField("electronic_minimizer", "a10"),
        ScalarField("nelectrons", float),
        ScalarField("nup", float),
        ScalarField("ndown", float),
        ScalarField("spin", float),
        ScalarField("charge", float),
        StrField("spin_treatment", "a20"),
    ),
    # The "original" cell
    "CELL%NUM_IONS": (ScalarField("num_ions_orig", int),),
    "CELL%MAX_IONS_IN_SPECIES": (ScalarField("max_ions_in_species_orig", int),),
    "CELL%REAL_LATTICE": (
        ArrayField(
            "real_lattice_orig",
            float,
            (
                3,
                3,
            ),
        ),
    ),
    "CELL%RECIP_LATTICE": (
        ArrayField(
            "recip_lattice_orig",
            float,
            (
                3,
                3,
            ),
        ),
    ),
    "CELL%NUM_SPECIES": (ScalarField("num_species_orig", int),),
    "CELL%NUM_IONS_IN_SPECIES": (
        ArrayField("num_ions_in_species_orig", int, ("num_species_orig",)),
    ),
    "CELL%IONIC_POSITIONS": (
        ArrayField(
            "ionic_positions",
            float,
            (3, "max_ions_in_species_orig", "num_species_orig"),
        ),
    ),
    "CELL%SPECIES_SYMBOL": (
        ArrayField("species_symbol_orig", "a8", ("num_species_orig",)),
    ),
    # The "current" cell
    "CELL%NUM_IONS_01": (ScalarField("num_ions", int),),
    "CELL%MAX_IONS_IN_SPECIES_01": (ScalarField("max_ions_in_species", int),),
    "CELL%REAL_LATTICE_01": (
        ArrayField(
            "real_lattice",
            float,
            (
                3,
                3,
            ),
        ),
    ),
    "CELL%RECIP_LATTICE_01": (
        ArrayField(
            "recip_lattice",
            float,
            (
                3,
                3,
            ),
        ),
    ),
    "CELL%NUM_SPECIES_01": (ScalarField("num_species", int),),
    "CELL%NUM_IONS_IN_SPECIES_01": (
        ArrayField("num_ions_in_species", int, ("num_species",)),
    ),
    "CELL%IONIC_POSITIONS_01": (
        ArrayField("ionic_positions", float, (3, "max_ions_in_species", "num_species")),
    ),
    "CELL%SPECIES_SYMBOL_01": (ArrayField("species_symbol", "a8", ("num_species",)),),
    "NKPTS_01": (ScalarField("nkpts", int),),
    "KPOINTS_01": (
        ArrayField("kpoints", float, shape=(3, "nkpts")),
    ),  # Kpoints in the original order
    "KPOINT_WEIGHTS_01": (
        ArrayField("kpoint_weights", float, shape=("nkpts",)),
    ),  # Weights in the original order
    # Parameters starts after the end of the global section of the "current" cell
    "END_CELL_GLOBAL_01": (
        BoolField(
            "found_ground_state_wavefunction"
        ),  # Fortran logical saved as integer....
        BoolField("found_ground_state_density"),
        ScalarField("total_energy", float),
        ScalarField("fermi_energy", float),
        CompositeField([ScalarField("nbands", int), ScalarField("nspins", int)]),
        EigenValueAndOccCompositeField(),  # Read the eigenvalues note that the arrays are reshaped
        BoolField("found_ground_state_density"),
        CompositeField(
            [
                ScalarField("ngx_fine", int),
                ScalarField("ngy_fine", int),
                ScalarField("ngz_fine", int),
            ]
        ),
        ChargeDensityField(),
    ),
    "E_FERMI": (ScalarField("fermi_energy_second_spin", float),),
    "FORCES": (ArrayField("forces", float, (3, "max_ions_in_species", "num_species")),),
    "STRESS": (ArrayField("stress", float, (6,)),),
    "FORCE_CON": (
        ArrayField("phonon_supercell_matrix", int, (3, 3)),
        ArrayField(
            "phonon_force_constant_matrix",
            float,
            (3, "num_ions", 3, "num_ions", "num_cells"),
        ),
        ArrayField("phonon_supercell_origins", int, (3, "num_cells")),
        ScalarField("phonon_force_constant_row", int),
    ),
    "BORN_CHGS": (ArrayField("born_charges", float, (3, 3, "num_ions")),),
}

# Specifications for the check file, the only difference is the additional wavefunction
# data taht is between the "nspins" and the "EigenValueAndOccCompositeField"
CASTEP_CHECK_FIELD_SPEC = {
    **CASTEP_BIN_FIELD_SPEC,
    "END_CELL_GLOBAL_01": (
        BoolField(
            "found_ground_state_wavefunction"
        ),  # Fortran logical saved as integer....
        BoolField("found_ground_state_density"),
        ScalarField("total_energy", float),
        ScalarField("fermi_energy", float),
        CompositeField([ScalarField("nbands", int), ScalarField("nspins", int)]),
        # Read the wave function
        StrField("wave_header", "a4"),
        CompositeField(
            [
                ScalarField("ngx", int),
                ScalarField("ngy", int),
                ScalarField("ngz", int),
            ]
        ),
        # Here starts the wavefunction relaxed data
        CompositeField(
            [
                ScalarField("wave_coeff_size_1", int),
                ScalarField("wave_spinorcomps", int),
                ScalarField("wave_nbands_max", int),
                ScalarField("wave_nkpts", int),
                ScalarField("wave_nspins", int),
            ]
        ),
        WaveFunctionField(),
        EigenValueAndOccCompositeField(),  # Read the eigenvalues note that the arrays are reshaped
        BoolField("found_ground_state_density"),
        CompositeField(
            [
                ScalarField("ngx_fine", int),
                ScalarField("ngy_fine", int),
                ScalarField("ngz_fine", int),
            ]
        ),
        ChargeDensityField(),
    ),
}

# Shape of each field
CASTEP_BIN_FIELD_SHAPES = {
    field.name: field.shape
    for value in CASTEP_BIN_FIELD_SPEC.values()
    for field in value
    if isinstance(field, ArrayField)
}


def read_castep_bin(
    filename: Union[str, Path] = None,
    fileobj=None,
    records_to_extract: Optional[Collection[str]] = None,
    spec=None,
) -> Dict[str, Any]:
    """
    Read a castep_bin file for a given CASTEP run.

    Fortran binary files consist of records, one for each Fortran `write`
    statement used to create the file. Each record is surrounded by
    a *record marker* that encodes the length of the record in bytes.

    The length of the record markers themselves are compiler-dependent,
    but ifort and gfortran 4.2+ have settled on 4-byte markers with an
    additional sign bit to indicate that more data follows.

    Further notes on this can be found in the documentation of the
    [FortranFiles.jl](https://traktofon.github.io/FortranFiles.jl/stable/files.html#Terminology-1)
    Julia package.

    CASTEP then additionally organises these records into sections
    denoted by string headers (with possible values from `CASTEP_BIN_HEADERS`),
    which themselves are Fortran file records.

    For example, a file might be structured like:

        <length of string header>
        <string header>
        <length of string header>
        <length of binary data in bytes (record marker)>
        <binary data>
        <length of binary data in bytes (record marker)>

    :param filename: path of the file to be read
    :param fileobj: An file-like object from which the data needs to be read
    :param records_to_extract: A collection of CASTEP bin headers. If `None`,
        all headers for which there is a defined shape specification in `CASTEP_BIN_HEADERS`.

    :returns: A dictionary following the CASTEP header hierarchy found within
    the castep_bin file, containing the decoded data.
    """

    def _read_handle(f):
        is_check, header_offset_map = _generate_header_offset_map(f)
        f.seek(0)

        castep_data = {}
        if spec is None:
            _spec = CASTEP_CHECK_FIELD_SPEC if is_check else CASTEP_BIN_FIELD_SPEC
        for header, field in _spec.items():

            if (
                records_to_extract
                and header not in records_to_extract
                and not header.startswith("CELL%")
            ):
                continue

            if header not in header_offset_map:
                if records_to_extract and header in records_to_extract:
                    raise RuntimeError(
                        f"Unable to find desired header {header} in file."
                    )
                continue

            castep_data.update(
                _decode_records(
                    f,
                    field,
                    header_offset_map[header],
                    castep_data,
                )
            )
        return castep_data

    if filename is not None:
        with open(filename, mode="rb") as fhandle:
            return _read_handle(fhandle)

    return _read_handle(fileobj)


def _decode_records(
    fp: io.BufferedReader,
    record_specs: Tuple[FieldType],
    offset: int,
    decoded_data: dict = None,
) -> Dict[str, Any]:
    """For a given file buffer, header name and byte offset, read
    the expected number of file records and decode them according to
    the type and shape specification provided in `CASTEP_BIN_HEADERS`.

    Note:
        The file buffer will not be reset to its initial position.

    Args:
        fp: The open file buffer.
        record_spec: An ordered dictionary with an entry per expected
            record, containing a tuple for `(dtype, shape)`. Unknown
            dimensions can be indicated by string values in `shape`.
            These unknowns will be resolved where possible and returned
            in the final output dictionary.
        offset: The byte offset at which the records start in the buffer.
        decoded_data: Data that has been decoded - need for getting array sizes.

    Returns:
        A dictionary containing the decoded data, and any named unknowns
        that were resolved in this pass.

    """
    if decoded_data is None:
        decoded_data = {}
    fp.seek(offset)
    for record_spec in record_specs:
        if isinstance(record_spec, FieldType):
            if isinstance(record_spec, SkippedField):
                record_spec.decode(fp)
                continue
            record_name = record_spec.name
            decoded_data[record_name] = record_spec.decode(fp, decoded_data)
        # This is a composite field
        elif isinstance(record_spec, CompositeField):
            # Read the decoded data
            record_data, _ = _read_record(fp)
            for subspec in record_spec.fields:
                offset = int(subspec.type_string[-1])
                if isinstance(subspec, ArrayField):
                    offset *= np.prod(subspec.resolve_shape(decoded_data)[0])
                assert offset > 0
                decoded_data[subspec.name] = subspec.decode(
                    fp, decoded_data, record_data=record_data
                )
                record_data = record_data[offset:]
        elif isinstance(record_spec, StructuredField):
            record_spec.decode(fp, decoded_data)

    return decoded_data


def _decode_composite(fp, record_spec):
    """Decode a composite field return the decoded data"""
    record_data, _ = _read_record(fp)
    decoded = []
    for subspec in record_spec.fields:
        offset = int(subspec.type_string[-1])
        if isinstance(subspec, ArrayField):
            offset *= np.prod(subspec.shape)
        assert offset > 0
        decoded.append(subspec.decode(fp, {}, record_data=record_data))
        record_data = record_data[offset:]
    return decoded


def _generate_header_offset_map(fileobj) -> Tuple[bool, Dict[str, int]]:
    """
    Scans a castep_bin/check file for recognisable headers, creating a
    dictionary of their byte-offsets within the file. The stored
    offset corresponds to the start of the record immediately
    following the CASTEP header.

    :param fileobj: A file object from which the data should be read.

    :returns: Tuple of (is_check, offset_map), where the latter is a dictionary of
    headers mapped to the offsets of the following record.
    """
    header_offset_map: Dict[str, int] = {}

    f = fileobj
    loc = f.tell()

    # Check first header is "CASTEP_BIN"
    header, _ = _read_record(f)
    header = header.decode("utf-8").strip("'")
    is_check = False
    if header != "CASTEP_BIN":
        is_check = True
        f.seek(loc)

    data = None
    while data != "END":
        data, _ = _read_record(f, seek_only=True)
        try:
            data = data.decode("utf-8").strip("'").strip()
            # Strip any non-alpha fields
            if data and data[0].isalpha() and data.upper() == data:
                # Check if this header already exists
                # for example, the cell information is written twice, one for the original cell
                # and the other for the 'current' cell
                if data in header_offset_map:
                    data = _find_header_suffix(data, header_offset_map)

                header_offset_map[data] = f.tell()
        except (AttributeError, UnicodeDecodeError):
            pass

    return is_check, header_offset_map


def _find_header_suffix(name, header_offset_map):
    """Found a suitable suffix the a given header name with number suffix"""
    counter = 1
    for key in header_offset_map.keys():
        match = re.match(f"{name}_(\\d+)", key)
        if match:
            num = int(match.group(1))
            if num >= counter:
                counter = num + 1
    return f"{name}_{counter:02d}"


def _read_record(
    f: io.BufferedReader,
    seek_only: bool = False,
    record_marker_size: int = 4,
    read_data_smaller_than=512,
) -> Tuple[Optional[bytes], int]:
    """Reads the preceeding record marker for the next record in the
    file, decodes the record data, then reads the suffix record marker,
    eventually returning the decoded record data.

    Args:
        f: The open binary file stream in the buffer.
        record_marker_size: The compiler-dependent size of the record
            marker used to indicate the data record size.
        seek_only: If `True`, do not read the data, but instead skip
            over it.
        read_data_smaller_than: read any data smaller than this number
            of bytes, taking precedence over `seek_only`.

    Returns:
        The byte data from the record, or None, if `seek_only` and the
        record exceeded the chosen size.

    """
    marker = _read_marker(f, record_marker_size=record_marker_size)
    data = None
    if marker <= read_data_smaller_than or not seek_only:
        data = f.read(marker)
    else:
        # seek from current stream position (SEEK_CUR), indicated by the 1
        f.seek(marker, 1)

    marker_end = _read_marker(f)
    if marker != marker_end:
        raise RuntimeError(
            f"The start ({marker}) and end ({marker_end}) record markers were inconsistent."
        )

    return data, marker


def _read_marker(
    f: Union[io.BufferedReader, bytes], record_marker_size: int = 4
) -> int:
    """Read the next *n* bytes from the buffer and try to interpret them
    as a Fortran record marker (typically uint4, but can depend on
    compiler).

    Args:
        f: An open file buffer.
        record_marker_size: The number of bytes to read as a record marker.

    Returns:
        The integer record marker.

    """

    if isinstance(f, io.BufferedReader):
        f = f.read(record_marker_size)

    return unpack(">I", f[:record_marker_size])[0]
