"""
Test the reader
"""
import os
from castep_bin_reader import read_pdos_bin

def test_pdos_reader():
    """Test the reader for pdos_bin"""

    filename = os.path.join(os.path.split(__file__)[0], 'test_data/Si2.pdos_bin')
    output = read_pdos_bin(filename)
    assert output['pdos_weights'].shape == (8, 23, 110, 1)