"""
Test the reader
"""
import os
import pytest
import numpy as np
import scipy.constants

from .pdos import read_pdos_bin, reorder_pdos_data, OrbitalEnum, SpinEnum
from .castep_bin import read_castep_bin

@pytest.fixture
def pdos_bin():
    return os.path.join(os.path.split(__file__)[0], 'test_data/Si2.pdos_bin')


@pytest.fixture
def bands_file():
    return os.path.join(os.path.split(__file__)[0], 'test_data/Si2.bands')


@pytest.fixture
def castep_bin_Si():
    """.castep_bin test file taken from Euphonic:
    https://github.com/pace-neutrons/Euphonic/blob/v0.6.2/tests_and_analysis/test/data/castep_files/Si2-sc-skew/Si2-sc-skew.castep_bin
    """
    return os.path.join(os.path.split(__file__)[0], 'test_data/Si2-sc-skew.castep_bin')

@pytest.fixture
def castep_bin_SiO2():
    """Binary output from a singlepoint with `calculate_stress: true`. """
    return os.path.join(os.path.split(__file__)[0], 'test_data/SiO2.castep_bin')


def test_pdos_reader(pdos_bin):
    """Test the reader for pdos_bin"""
    output = read_pdos_bin(pdos_bin)
    assert output['pdos_weights'].shape == (8, 23, 110, 1)


def test_pdos_reorder(pdos_bin):
    """Test reordering of the PDOS"""
    try:
        from pymatgen.electronic_structure.core import Orbital as POrbital
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
        "phonon_force_constant_row"
    )
    assert all(field in data for field in expected_fields)
    assert data["forces"].shape == (3, data["max_ions_in_species"], data["num_species"])
    assert data["phonon_force_constant_matrix"].shape == (3, data["num_ions"], 3, data["num_ions"], data["num_cells"])

    # Check that the same parsing works even if cell info is missing (e.g., test recursive dimension solving)
    data = read_castep_bin(castep_bin_Si, records_to_extract=("FORCES", "CELL%MAX_IONS_IN_SPECIES"))

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
        "phonon_force_constant_row"
    )
    assert all(field in data for field in expected_fields)
    assert data["phonon_force_constant_matrix"].shape == (3, data["num_ions"], 3, data["num_ions"], data["num_cells"])

    # Check that process fails safely when not enough info is available
    with pytest.raises(RuntimeError, match=r"Too many unknowns to resolve*"):
        data = read_castep_bin(castep_bin_Si, records_to_extract=("FORCES"))

    # Check forces are consistent with castep file with multiple species
    data = read_castep_bin(castep_bin_SiO2)
    assert "forces" in data
    ev_per_ang_to_hartree_per_bohr = 1e10 * scipy.constants.physical_constants["Bohr radius"][0] / scipy.constants.physical_constants["Hartree energy in eV"][0]
    expected_forces = np.array([
        [ 0.00017, -0.40797,  0.00006],
        [ 0.40772,  0.00029,  0.00006],
        [ 0.00017,  0.40765, -0.00018],
        [-0.40773, -0.00042,  0.00003],
        [-0.00052,  0.00009, -0.00007],
        [ 0.00018,  0.00038,  0.00010]
        ]) * ev_per_ang_to_hartree_per_bohr

    # Compare the arrays per species
    np.testing.assert_array_almost_equal(expected_forces[0:4], data["forces"][:, :, 0].T)
    np.testing.assert_array_almost_equal(expected_forces[4:], data["forces"][:, :, 1].T[:2, :])
