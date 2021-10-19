"""
Test the reader
"""
import os
import pytest
import numpy as np

from .pdos import read_pdos_bin, reorder_pdos_data, compute_pdos
from .castep_bin import read_castep_bin
from pymatgen.electronic_structure.core import Orbital, Spin


@pytest.fixture
def pdos_bin():
    return os.path.join(os.path.split(__file__)[0], 'test_data/Si2.pdos_bin')


@pytest.fixture
def bands_file():
    return os.path.join(os.path.split(__file__)[0], 'test_data/Si2.bands')


@pytest.fixture
def castep_bin():
    """.castep_bin test file taken from Euphonic:
    https://github.com/pace-neutrons/Euphonic/blob/v0.6.2/tests_and_analysis/test/data/castep_files/Si2-sc-skew/Si2-sc-skew.castep_bin
    """
    return os.path.join(os.path.split(__file__)[0], 'test_data/Si2-sc-skew.castep_bin')


def test_pdos_reader(pdos_bin):
    """Test the reader for pdos_bin"""
    output = read_pdos_bin(pdos_bin)
    assert output['pdos_weights'].shape == (8, 23, 110, 1)


def test_pdos_reorder(pdos_bin):
    """Test reordering of the PDOS"""
    raw_output = read_pdos_bin(pdos_bin)
    reordered = reorder_pdos_data(raw_output)
    assert reordered[0][Orbital.s][Spin.up].shape == (23, 110)


@pytest.mark.skip("Skip due lastest sumo being unavailable")
def test_pdos_compute(pdos_bin, bands_file):
    """Test computing pdos"""
    from sumo.io.castep import (_read_bands_header_verbose,
                                read_bands_eigenvalues, _is_metal, _get_vbm,
                                _ry_to_ev)

    header = _read_bands_header_verbose(bands_file)
    _, weights, eigenvalues = read_bands_eigenvalues(bands_file, header)

    bin_width = 0.01
    bins = np.arange(0.0, 10.0 + bin_width, bin_width)

    pdos = compute_pdos(pdos_bin, eigenvalues, weights, bins)


def test_castep_bin_reader(castep_bin):
    if not os.path.isfile(castep_bin):
        pytest.skip(".castep_bin test data is missing")
    data = read_castep_bin(castep_bin)
    expected_fields = (
        "num_ions",
        "num_cells",
        "num_species",
        "max_ions_in_species",
        "forces",
        "phonon_supercell_matrix",
        "phonon_force_constant_matrix",
        "phonon_supercell_origins",
        "phonon_force_constant_row"
    )
    assert all(field in data for field in expected_fields)
    assert data["forces"].shape == (3, data["max_ions_in_species"], data["num_species"])
    assert data["phonon_force_constant_matrix"].shape == (3, data["num_ions"], 3, data["num_ions"], data["num_cells"])

    # Check that the same parsing works even if cell info is missing (e.g., test recursive dimension solving)
    data = read_castep_bin(castep_bin, records_to_extract=("FORCES", "CELL%MAX_IONS_IN_SPECIES"))

    expected_fields = (
        "num_species",
        "max_ions_in_species",
        "forces",
    )
    assert all(field in data for field in expected_fields)
    assert data["forces"].shape == (3, data["max_ions_in_species"], data["num_species"])

    # Check that indivdual blocks can resolve self-consistently
    # (the value of num_ions or num_cells are not read) from the castep_bin
    data = read_castep_bin(castep_bin, records_to_extract=("FORCE_CON"))

    expected_fields = (
        "num_ions",
        "num_cells",
        "phonon_supercell_matrix",
        "phonon_force_constant_matrix",
        "phonon_supercell_origins",
        "phonon_force_constant_row"
    )
    assert all(field in data for field in expected_fields)
    assert data["phonon_force_constant_matrix"].shape == (3, data["num_ions"], 3, data["num_ions"], data["num_cells"])

    # Check that process fails safely when not enough info is available
    with pytest.raises(RuntimeError, match=r"Too many unknowns to resolve*"):
        data = read_castep_bin(castep_bin, records_to_extract=("FORCES"))
