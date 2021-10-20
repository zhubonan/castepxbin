"""
Test the reader
"""
import os
import pytest
import numpy as np

from .pdos import read_pdos_bin, reorder_pdos_data, compute_pdos
from .ome_bin import read_ome_bin, read_cst_ome
from pymatgen.electronic_structure.core import Orbital, Spin


@pytest.fixture
def pdos_bin():
    return os.path.join(os.path.split(__file__)[0], 'test_data/Si2.pdos_bin')

@pytest.fixture
def ome_bin():
    return os.path.join(os.path.split(__file__)[0], 'test_data/Si2.ome_bin')

@pytest.fixture
def cst_ome():
    return os.path.join(os.path.split(__file__)[0], 'test_data/Si2.cst_ome')

@pytest.fixture
def bands_file():
    return os.path.join(os.path.split(__file__)[0], 'test_data/Si2.bands')


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
    assert np.imag(om[0, 0, 1, -1, -1]) == pytest.approx(0.0)