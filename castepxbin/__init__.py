"""
Collection of binary file readers for CASTEP
"""
from .pdos import compute_pdos, read_pdos_bin
from .castep_bin import read_castep_bin
from .ome_bin import read_dome_bin, read_cst_ome, read_ome_bin

__version__ = "0.2.0"
