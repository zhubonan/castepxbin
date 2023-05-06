"""
Functions for handling wave function related data
"""

from typing import BinaryIO

import numpy as np

from .castep_bin import read_castep_bin


def coords_to_indices(grid_coords: np.ndarray, grid_size: np.ndarray):
    """
    Convert reciprocal lattice indexing to a grid
    based indices. This is allows reconstruct the wave function
    on to a reciprocal space grid.
    """

    indices = grid_coords.copy()
    grid_size = np.asarray(grid_size)
    grid_size = grid_size[:, np.newaxis, np.newaxis]
    indices = grid_coords % grid_size
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


class WaveFunction:  # pylint:disable=too-many-instance-attributes
    """
    Class for handling the wave function
    """

    def __init__(
        self,
        coeffs,
        pw_grid_coords,
        mesh_size,
        nwaves_at_kp,
        kpts,
        recip_lattice,
        real_lattice,
        eigenvalues,
        occupancies,
        fermi_energy,
        data=None,
    ):
        """Instantiate weave function reader"""

        self.coeffs = coeffs
        (
            self.nwave_max,
            self.nspinors,
            self.nbands,
            self.nkpts,
            self.nspins,
        ) = coeffs.shape
        if data is None:
            data = {}
        self.data = data
        self.fermi_energy = fermi_energy
        self.nwaves_at_kp = nwaves_at_kp
        self.pw_grid_coords = pw_grid_coords
        self.mesh_size = mesh_size
        self.kpts = kpts
        self.pw_grid_indices = coords_to_indices(self.pw_grid_coords, self.mesh_size)
        # CASTEP stores the lattice matrix with row vectors - these are all in atomic units
        self.recip_lattice = recip_lattice
        self.real_lattice = real_lattice
        self.occupancies = occupancies
        self.eigenvalues = eigenvalues
        # Orbital files from bandstructure/spectral calculations do no contain occupancies
        # Here we naively occupy all states below the fermi level...
        if self.occupancies.sum() == 0:
            self.occupancies[self.eigenvalues < self.fermi_energy] = 1.0

    @classmethod
    def from_dict(cls, full_data):
        """
        Load a WaveFunction object from a dictionary parsed from the
        check file.
        """
        wfc = full_data["wavefunction"]
        mesh = np.array([wfc["ngx"], wfc["ngy"], wfc["ngz"]])
        inputd = {"mesh_size": mesh}
        for key in ["coeffs", "pw_grid_coords", "nwaves_at_kp", "kpts"]:
            inputd[key] = wfc[key]

        for key in [
            "real_lattice",
            "recip_lattice",
            "eigenvalues",
            "occupancies",
            "fermi_energy",
        ]:
            inputd[key] = full_data[key]
        inputd["data"] = full_data

        return cls(**inputd)

    @classmethod
    def from_file(cls, fname: BinaryIO):
        """
        Load directly from a file or a file object

        :param fname: Name of the file or a file-like object.
        """
        if hasattr(fname, "read"):
            data = read_castep_bin(fileobj=fname)
        else:
            data = read_castep_bin(filename=fname)
        return cls.from_dict(data)

    def get_reciprocal_grid(self) -> np.ndarray:
        """
        Return an on grid representation of the wavefunction
        """

        return coeff_to_recip(
            self.coeffs, self.nwaves_at_kp, self.pw_grid_coords, *self.mesh_size
        )

    def get_plane_wave_coeffs(self, ispin=0, ik=0, ib=0, ispinor=0):
        """
        Return plane wave coefficients
        """
        return self.coeffs[: self.nwaves_at_kp[ik], ispinor, ib, ik, ispin]

    def get_gvectors(self, ik=0):
        """
        Return gvectors in the unit of reciprocal lattice vectors
        """
        return self.pw_grid_coords[:, : self.nwaves_at_kp[ik], ik]

    def get_gmesh_index(self, ik=0):
        """
        Return indices of the mesh for each plane wave coefficient at K
        """
        return self.pw_grid_indices[:, : self.nwaves_at_kp[ik], ik]

    def get_kpoints_cart(self):
        """
        Return the cartesian coordinates of the k-points

        ```{note}
        These are in the internal atomic units used by CASTEP.
        ```
        """
        return self.recip_lattice.T @ self.kpts
