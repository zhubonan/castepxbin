"""
Test the reader
"""
import io
import os
import struct

import numpy as np
import pytest
import scipy.constants

from castepxbin._dtypes import endian_symbol
from castepxbin.castep_bin import (
    ArrayField,
    CompositeField,
    ScalarField,
    StrField,
    _decode_composite,
    read_castep_bin,
)
from castepxbin.ome_bin import read_cst_ome, read_dome_bin, read_ome_bin
from castepxbin.pdos import (
    OrbitalEnum,
    SpinEnum,
    read_pdos_bin,
    reorder_pdos_data,
)
from castepxbin.wave import coeff_to_recip, coords_to_indices


@pytest.fixture
def pdos_bin():
    return os.path.join(os.path.split(__file__)[0], "test_data/Si2.pdos_bin")


@pytest.fixture
def ome_bin():
    return os.path.join(os.path.split(__file__)[0], "test_data/Si2.ome_bin")


@pytest.fixture
def cst_ome():
    return os.path.join(os.path.split(__file__)[0], "test_data/Si2.cst_ome")


@pytest.fixture
def dome_bin():
    return os.path.join(os.path.split(__file__)[0], "test_data/Si2.dome_bin")


@pytest.fixture
def bands_file():
    return os.path.join(os.path.split(__file__)[0], "test_data/Si2.bands")


@pytest.fixture
def castep_bin_Si():
    """.castep_bin test file taken from Euphonic:
    https://github.com/pace-neutrons/Euphonic/blob/v0.6.2/tests_and_analysis/test/data/castep_files/Si2-sc-skew/Si2-sc-skew.castep_bin
    """
    return os.path.join(os.path.split(__file__)[0], "test_data/Si2-sc-skew.castep_bin")


@pytest.fixture
def castep_check_Si():
    """.check test file taken from Euphonic:
    https://github.com/pace-neutrons/Euphonic/blob/v0.6.2/tests_and_analysis/test/data/castep_files/Si2-sc-skew/Si2-sc-skew.castep_bin
    """
    return os.path.join(os.path.split(__file__)[0], "test_data/Si2.check")


@pytest.fixture
def castep_bin_SiO2():
    """Binary output from a singlepoint with `calculate_stress: true`."""
    return os.path.join(os.path.split(__file__)[0], "test_data/SiO2.castep_bin")


def test_pdos_reader(pdos_bin):
    """Test the reader for pdos_bin"""
    output = read_pdos_bin(pdos_bin)
    assert output["pdos_weights"].shape == (8, 23, 110, 1)


def test_pdos_reorder(pdos_bin):
    """Test reordering of the PDOS"""
    try:
        from pymatgen.electronic_structure.core import (
            Orbital as POrbital,
        )
        from pymatgen.electronic_structure.core import Spin as PSpin
    except ImportError:
        pass
    else:
        raw_output = read_pdos_bin(pdos_bin)
        reordered = reorder_pdos_data(raw_output)
        assert reordered[0][POrbital.s][PSpin.up].shape == (23, 110)

    raw_output = read_pdos_bin(pdos_bin)
    reordered = reorder_pdos_data(raw_output, pymatgen_labels=False)
    assert reordered[0][OrbitalEnum.s][SpinEnum.up].shape == (23, 110)


def test_castep_check_reader(castep_check_Si):

    data = read_castep_bin(castep_check_Si)
    assert "wavefunction" in data
    wfc = data["wavefunction"]
    assert "ngx" in wfc
    assert "pw_grid_coords" in wfc
    assert "coeffs" in wfc
    assert "kpts" in wfc
    assert "nwaves_at_kp" in wfc
    mesh_size = np.array([wfc["ngx"], wfc["ngy"], wfc["ngz"]])
    idx = coords_to_indices(wfc["pw_grid_coords"], mesh_size)
    assert idx.min() == 0
    assert idx.max() == mesh_size.max() - 1
    grid = coeff_to_recip(
        wfc["coeffs"], wfc["nwaves_at_kp"], wfc["pw_grid_coords"], *mesh_size
    )

    from castepxbin.wave import WaveFunction

    wf = WaveFunction.from_dict(data)
    mesh = wf.get_reciprocal_grid()
    assert np.array_equal(mesh.shape[:3], wf.mesh_size)

    assert wf.get_plane_wave_coeffs().size > 0
    assert (
        wf.get_plane_wave_coeffs(
            ik=wf.nkpts - 1, ib=wf.nbands - 1, ispin=wf.nspins - 1
        ).size
        > 0
    )
    assert wf.get_gvectors().size > 0
    assert wf.get_gvectors(ik=wf.nkpts - 1).size > 0
    assert wf.get_gmesh_index().size > 0
    assert wf.get_gmesh_index(ik=wf.nkpts - 1).size > 0
    assert isinstance(wf.get_kpoints_cart(), np.ndarray)


def test_castep_bin_reader(castep_bin_Si, castep_bin_SiO2):
    if not os.path.isfile(castep_bin_Si):
        pytest.skip(".castep_bin test data is missing")
    data = read_castep_bin(castep_bin_Si)
    expected_fields = (
        "num_ions",
        "num_cells",
        "num_species",
        "max_ions_in_species",
        "forces",
        "phonon_supercell_matrix",
        "phonon_force_constant_matrix",
        "phonon_supercell_origins",
        "phonon_force_constant_row",
    )
    assert all(field in data for field in expected_fields)
    assert data["forces"].shape == (3, data["max_ions_in_species"], data["num_species"])
    assert data["phonon_force_constant_matrix"].shape == (
        3,
        data["num_ions"],
        3,
        data["num_ions"],
        data["num_cells"],
    )

    # Check that the same parsing works even if cell info is missing (e.g., test recursive dimension solving)
    data = read_castep_bin(
        castep_bin_Si, records_to_extract=("FORCES", "CELL%MAX_IONS_IN_SPECIES_01")
    )

    expected_fields = (
        "num_species",
        "max_ions_in_species",
        "forces",
    )
    assert all(field in data for field in expected_fields)
    assert data["forces"].shape == (3, data["max_ions_in_species"], data["num_species"])
    # Check that indivdual blocks can resolve self-consistently
    # (the value of num_ions or num_cells are not read) from the castep_bin
    data = read_castep_bin(castep_bin_Si, records_to_extract=("FORCE_CON"))

    expected_fields = (
        "num_ions",
        "num_cells",
        "phonon_supercell_matrix",
        "phonon_force_constant_matrix",
        "phonon_supercell_origins",
    )
    assert all(field in data for field in expected_fields)
    assert data["phonon_force_constant_matrix"].shape == (
        3,
        data["num_ions"],
        3,
        data["num_ions"],
        data["num_cells"],
    )

    # Check forces are consistent with castep file with multiple species
    data = read_castep_bin(castep_bin_SiO2)
    assert "forces" in data
    assert data.get("found_ground_state_density") is True
    assert data.get("found_ground_state_wavefunction") is True
    assert data.get("total_energy") == pytest.approx(-77.0824329248417)
    assert data.get("nbands") == 20
    assert data.get("nspins") == 2
    assert data.get("nkpts") == 14
    assert data.get("kpoints").shape == (3, 14)
    assert data.get("kpoints_of_eigenvalues").shape == (3, 14)
    assert data.get("eigenvalues").shape == (20, 14, 2)
    assert data.get("occupancies")[0, 0, 0] == 1.0

    ev_per_ang_to_hartree_per_bohr = (
        1e10
        * scipy.constants.physical_constants["Bohr radius"][0]
        / scipy.constants.physical_constants["Hartree energy in eV"][0]
    )
    expected_forces = (
        np.array(
            [
                [0.00017, -0.40797, 0.00006],
                [0.40772, 0.00029, 0.00006],
                [0.00017, 0.40765, -0.00018],
                [-0.40773, -0.00042, 0.00003],
                [-0.00052, 0.00009, -0.00007],
                [0.00018, 0.00038, 0.00010],
            ]
        )
        * ev_per_ang_to_hartree_per_bohr
    )

    # Compare the arrays per species
    np.testing.assert_allclose(
        expected_forces[0:4], data["forces"][:, :, 0].T, atol=1e-6
    )
    np.testing.assert_allclose(
        expected_forces[4:], data["forces"][:, :, 1].T[:2, :], atol=1e-6
    )

    # `np.frombuffer` hands back read-only views over the record buffer - the
    # reader must copy so that callers can work with the arrays in place.
    for key in ("forces", "real_lattice", "kpoints", "ionic_positions"):
        assert data[key].flags.writeable, f"{key} is read-only"
    data["forces"] += 0.0

    # Test reading all fields
    fobj = open(castep_bin_SiO2, "rb")
    data = read_castep_bin(fileobj=fobj, records_to_extract=None)
    expected_fields = (
        "num_ions",
        "real_lattice",
        "recip_lattice",
        "num_ions_in_species",
        "ionic_positions",
        "species_symbol",
        "num_species",
        "spin_density",
        "charge_density",
        "ngz_fine",
        "spin_treatment",
    )

    for field in expected_fields:
        assert field in data
    assert data["num_species"] == 2
    assert data["ionic_positions"].shape == (
        3,
        data["max_ions_in_species"],
        data["num_species"],
    )
    assert data["species_symbol"] == ["O", "Si"]
    assert data["spin_treatment"] == "SCALAR"
    fobj.close()


def test_ome_bin(ome_bin):
    """Test reading ome_bin file"""
    v, header, om = read_ome_bin(ome_bin, 23, 2, 1)
    assert "CASTEP" in header
    assert v == pytest.approx(1.0)
    assert om.shape == (1, 2, 3, 23, 23)
    assert np.imag(om[0, 0, 1, 0, 0]) == pytest.approx(0.0)


def test_cst_ome(cst_ome):
    """Test reading ome_bin file"""
    om = read_cst_ome(cst_ome, 23, 2, 1)
    assert om.shape == (1, 2, 3, 23, 23)
    assert om.dtype == np.dtype(complex)
    assert np.imag(om[0, 0, 1, -1, -1]) == pytest.approx(0.0)

    # Values pinned against the original record-by-record reader
    assert om[0, 0, 0, 0, 0] == pytest.approx(-0.23182434794017326)
    assert om[0, 0, 1, -1, -1] == pytest.approx(0.8834243620378435)
    assert om[0, 1, 2, 5, 7] == pytest.approx(
        0.06673646712344057 + 0.10960926081880899j
    )
    assert om[0, 0, 0, 0, 1] == pytest.approx(0.1710798190590074 - 0.01683650302237705j)

    with open(cst_ome, "rb") as fhandle:
        assert np.array_equal(read_cst_ome(fhandle, 23, 2, 1), om)


def test_cst_ome_size_mismatch(cst_ome):
    """Wrong array sizes must be reported, not silently mis-read"""
    with pytest.raises(ValueError, match="Expected"):
        read_cst_ome(cst_ome, 23, 2, 2)
    with pytest.raises(ValueError, match="record markers"):
        read_cst_ome(cst_ome, 23, 2, 1, endian="little")


def test_dome_bin(dome_bin):
    """Test reading ome_bin file"""
    v, header, dom = read_dome_bin(dome_bin, 23, 2, 1)

    assert "CASTEP" in header
    assert v == pytest.approx(1.0)

    assert dom.shape == (1, 2, 3, 23)
    assert dom[0, 0, 0, 0] == pytest.approx(-0.09854794)


def _fortran_record(payload: bytes) -> io.BufferedReader:
    """Wrap a payload in the 4 byte record markers CASTEP writes.

    `_read_marker` checks for an `io.BufferedReader`, so a bare `io.BytesIO`
    is not enough.
    """
    marker = struct.pack(">I", len(payload))
    return io.BufferedReader(io.BytesIO(marker + payload + marker))


@pytest.mark.parametrize(
    "field,itemsize,kind",
    [
        (ScalarField("x", int), 4, "i"),
        (ScalarField("x", float), 8, "f"),
        (ScalarField("x", complex), 16, "c"),
        (StrField("x", "S4"), 4, "S"),
        (StrField("x", "S8"), 8, "S"),
        (StrField("x", "S10"), 10, "S"),
        (StrField("x", "S20"), 20, "S"),
    ],
)
def test_field_dtype_metadata(field, itemsize, kind):
    """Every dtype the specs build must report its own size and kind."""
    assert field.dtype.itemsize == itemsize
    assert field.dtype.kind == kind


def test_composite_complex_subfield_stride():
    """A c16 subfield must advance the record buffer by 16 bytes, not 6."""
    payload = (
        np.array([1 + 2j], dtype=">c16").tobytes()
        + np.array([42], dtype=">i4").tobytes()
    )
    spec = CompositeField([ScalarField("zval", complex), ScalarField("nwaves", int)])
    assert _decode_composite(_fortran_record(payload), spec) == [1 + 2j, 42]


def test_composite_string_subfield_stride():
    """An S10 subfield must advance the record buffer by 10 bytes, not 0."""
    payload = b"PBE       " + np.array([7], dtype=">i4").tobytes()
    spec = CompositeField([StrField("tag", "S10"), ScalarField("n", int)])
    assert _decode_composite(_fortran_record(payload), spec) == ["PBE", 7]


def test_composite_float_array_subfield():
    """Regression guard for the one composite shape used in the shipped specs."""
    payload = (
        np.array([1.0, 2.0, 3.0], dtype=">f8").tobytes()
        + np.array([9], dtype=">i4").tobytes()
    )
    spec = CompositeField([ArrayField("kpt", float, (3,)), ScalarField("nwaves", int)])
    kpt, nwaves = _decode_composite(_fortran_record(payload), spec)
    np.testing.assert_array_equal(kpt, [1.0, 2.0, 3.0])
    assert nwaves == 9


@pytest.mark.parametrize(
    "endian,expected",
    [("BIG", ">"), ("big", ">"), ("Big", ">"), ("LITTLE", "<"), ("little", "<")],
)
def test_endian_symbol(endian, expected):
    assert endian_symbol(endian) == expected


def test_endian_symbol_rejects_unknown():
    with pytest.raises(ValueError, match="Unknown endianness"):
        endian_symbol("middle")


def test_pdos_endian_is_honoured(pdos_bin):
    """The fixture is big-endian; reading it as little-endian must not succeed."""
    from scipy.io import FortranFormattingError

    with pytest.raises((FortranFormattingError, ValueError)):
        read_pdos_bin(pdos_bin, endian="little")


def _coeff_to_recip_reference(coeffs, nwaves_at_kp, grid_coords, ngx, ngy, ngz):
    """The original element-by-element scatter, kept as a reference."""
    _, nspinor, band_max, nkpts, nspins = coeffs.shape
    indices = coords_to_indices(grid_coords, (ngx, ngy, ngz))
    grid = np.zeros(
        (ngx, ngy, ngz, nspinor, band_max, nkpts, nspins), order="F", dtype=complex
    )
    for ispin in range(nspins):
        for ik in range(nkpts):
            for ib in range(band_max):
                for ispinor in range(nspinor):
                    for ipw in range(nwaves_at_kp[ik]):
                        grid[
                            indices[0, ipw, ik],
                            indices[1, ipw, ik],
                            indices[2, ipw, ik],
                            ispinor,
                            ib,
                            ik,
                            ispin,
                        ] = coeffs[ipw, ispinor, ib, ik, ispin]
    return grid


def test_coeff_to_recip_matches_reference(castep_check_Si):
    """The vectorised scatter must be exactly equal to the original loop."""
    wfc = read_castep_bin(castep_check_Si)["wavefunction"]
    mesh = (wfc["ngx"], wfc["ngy"], wfc["ngz"])
    args = (wfc["coeffs"], wfc["nwaves_at_kp"], wfc["pw_grid_coords"], *mesh)
    assert np.array_equal(coeff_to_recip(*args), _coeff_to_recip_reference(*args))


def test_coeff_to_recip_multiple_spins_and_spinors():
    """The Si2 fixture has nspinor == nspins == 1, so cover the rest here."""
    rng = np.random.default_rng(0)
    ngx, ngy, ngz, nspinor, nbands, nkpts, nspins = 4, 5, 6, 2, 3, 4, 2
    npw_max = 7
    nwaves_at_kp = np.array([7, 5, 3, 1])
    grid_coords = rng.integers(-9, 9, size=(3, npw_max, nkpts))
    shape = (npw_max, nspinor, nbands, nkpts, nspins)
    coeffs = rng.normal(size=shape) + 1j * rng.normal(size=shape)
    args = (coeffs, nwaves_at_kp, grid_coords, ngx, ngy, ngz)
    assert np.array_equal(coeff_to_recip(*args), _coeff_to_recip_reference(*args))
