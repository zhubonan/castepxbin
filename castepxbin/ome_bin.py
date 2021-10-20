"""
Module for reading OME_BIN/CST_OME file
"""
import numpy as np
from scipy.io import FortranFile

__all__ = ["read_ome_bin", "read_cst_ome"]

def read_ome_bin(fname, num_bands, num_kpoints, num_spins, endian='big'):
    """
    Read the ome_bin file. 

    Note that we return the data in the 'C' order with dimensions (num_spins, num_kpoints, 3, num_bands, num_bands)
    
    Args:
        fname: Name of the file.
        num_bands: Number of bands.
        num_kpoints: Number of kpoints.
        num_spins: Number of spins.
        endian: Endian - CASTEP build instruction defaults to big-endian.

    Returns:
        version: The version number stored in the file.
        header: Header part written in the file.
        om: Optical matrix with dimensions (num_spins, num_kpoins, 3, num_bands, num_bands)
    """

    esymbol = '>' if endian.upper() == 'BIG' else '<'
    version_dtype = '{}f8'.format(esymbol)
    header_dtype = '{}a80'.format(esymbol)
    # Each complex number takes 2*8 bits - both real and imaginary parts are 
    # double precision
    array_seg = '{}(3,{},{})c16'.format(esymbol, num_bands, num_bands)

    om = np.zeros((num_spins, num_kpoints, 3, num_bands, num_bands), dtype=complex)
    with FortranFile(fname, header_dtype=np.dtype(f'{esymbol}u4')) as fhandle:
        version = fhandle.read_record(version_dtype)
        header = fhandle.read_record(header_dtype)[0].decode()
        for ki in range(num_kpoints):
            for si in range(num_spins):
                d = fhandle.read_record(array_seg)
                om[si, ki, :, :, :] = d
    return version[0], header, om


def read_cst_ome(fname, num_bands, num_kpoints, num_spins, endian='big'):
    """
    Read the ome_bin file. 

    Note that we return the data in the 'C' order with dimensions (num_spins, num_kpoints, 3, num_bands, num_bands)
    
    Args:
        fname: Name of the file.
        num_bands: Number of bands.
        num_kpoints: Number of kpoints.
        num_spins: Number of spins.
        endian: Endian - CASTEP build instruction defaults to big-endian.

    Returns:
        om: Optical matrix with dimensions (num_spins, num_kpoins, 3, num_bands, num_bands)
    """

    esymbol = '>' if endian.upper() == 'BIG' else '<'
    # Each complex number takes 2*8 bits - both real and imaginary parts are 
    # double precision
    elem = '{}c16'.format(esymbol, num_bands, num_bands)

    om = np.zeros((num_spins, num_kpoints, 3, num_bands, num_bands), dtype=complex)
    with FortranFile(fname, header_dtype=np.dtype(f'{esymbol}u4')) as fhandle:
        for ki in range(num_kpoints):
            for si in range(num_spins):
                for idx in range(3):
                    for ib1 in range(num_bands):
                        for ib2 in range(num_bands):
                            om[si, ki, idx, ib1, ib2] = fhandle.read_record(elem)
        out = fhandle._fp.read()
        assert out == b"", "More data exist beyond the specified sizes."
    return om


def read_dome_bin(fname, num_bands, num_kpoints, num_spins, endian="BIG"):
    """
    Read the dome_bin file
    """

    # Each complex number takes 2*8 bits - both real and imaginary parts are 
    # double precision
    esymbol = '>' if endian.upper() == 'BIG' else '<'
    version_dtype = '{}f8'.format(esymbol)
    header_dtype = '{}a80'.format(esymbol)
    array_seg = '{}(3,{})f8'.format(esymbol, num_bands)

    dom = np.zeros((num_spins, num_kpoints, 3, num_bands), dtype=float)
    with FortranFile(fname, header_dtype=np.dtype(f'{esymbol}u4')) as fhandle:
        version = fhandle.read_record(version_dtype)
        header = fhandle.read_record(header_dtype)[0].decode()
        for ki in range(num_kpoints):
            for si in range(num_spins):
                d = fhandle.read_record(array_seg)
                dom[si, ki, :, :] = d
    return version[0], header, dom