"""
Test the reader
"""
import os
import pytest
import numpy as np

from .pdos import read_pdos_bin, reorder_pdos_data, compute_pdos, OrbitalEnum, SpinEnum
from pymatgen.electronic_structure.core import Orbital as POrbital
from pymatgen.electronic_structure.core import Spin as PSpin


@pytest.fixture
def pdos_bin():
    return os.path.join(os.path.split(__file__)[0], 'test_data/Si2.pdos_bin')


@pytest.fixture
def bands_file():
    return os.path.join(os.path.split(__file__)[0], 'test_data/Si2.bands')


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

    reordered = reorder_pdos_data(raw_output, pymatgen_labels=False)
    assert reordered[0][OrbitalEnum.s][SpinEnum.up].shape == (23, 110)