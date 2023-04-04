"""
Functions for handling wave function related data
"""

import numpy as np


def coords_to_indices(grid_coords: np.ndarray, grid_size: np.ndarray):
    """
    Convert reciprocal lattice indexing to a grid
    based indices. This is allows reconstruct the wave function
    on to a reciprocal space grid.
    """

    indices = grid_coords.copy()
    _, npw, nkpts = grid_coords.shape

    for ikpt in range(nkpts):
        for ipw in range(npw):
            for i in range(3):
                if indices[i, ipw, ikpt] < 0:
                    indices[i, ipw, ikpt] += grid_size[i]
    return indices


def coeff_to_recip(
    coeffs: np.ndarray,
    nwaves_at_kp: np.ndarray,
    grid_coords: np.ndarray,
    ngx: int,
    ngy: int,
    ngz: int,
):
    """
    Convert compact coefficient representation to a full reciprocal
    grid representation for the wave function. The output data is on a 3D grid
    that is ready to be inverse FFTed.

    :param coeffs: Plane wave coefficients, in the shape of (npw, nspinor, nb, nk, nspins)

    :return: The plane wave coefficients on the grid, in the shape of (ngx, ngy, ngz, nspinor, nband, nk, nspins)
    """

    _, nspinor, band_max, nkpts, nspins = coeffs.shape
    grid_size = (ngx, ngy, ngz)
    indices = coords_to_indices(grid_coords, grid_size)

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
