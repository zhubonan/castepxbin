# Usage

This package only provides basic, low level interfaces for reading data rather than performing any analysis.

No unit conversion is carried out - any numerical values returned are simply in the internal unit used by CASTEP.
In most cases, they are in the [atomic units](https://en.wikipedia.org/wiki/Hartree_atomic_units).


To convert to SI-based units, one can use `ase.units`:

```python
from castepxbin import castep_bin import read_castep_bin
from ase.units import Hartree

data = read_castep_bin(filename='<path to .castep_bin or .check>')
print("One Ha is {Hartree} eV")

fermi_energy_in_eV = data['fermi_energy'] * Hartree
```

## Supported files

pdos_bin
: Stores the weights projected onto atomic orbitals for each band. This file is necessary for constructing *projected density of states*. This file is only written with `pdos_calculate_weights : true` in the *param* file.
Use {py:func}`read_pdos_bin<castepxbin.pdos.read_pdos_bin>` to parse this file. It returns a dictionary of arrays.

  The arrays are not arranged in the most sensible way and one may want to use {py:func}`reorder_pdos_data<castepxbin.pdos.reorder_pdos_data>` to process it so the species, ion number and orbitals are assigned.
The {py:func}`compute_pdos<castepxbin.pdos.compute_pdos>` function can be used to obtain the projected-density of states,
but one needs to supply the eigenvalues (mind the units) and the weighting of the kpoints.

ome_bin
: Stores the optical matrix elements from a `task : spectral` calculation with *spectral_task* being one of *optics*, *coreless*, *all*.

dome_bin
: Stores the diagonal elements of the optical matrix from a `task : spectral` calculation with *spectral_task* being *dos*.

cst_ome
: Stores the optical matrix elements from a `task : optics` calculation.

check
: Stores most calculated quantities and can be used for restarting a calculation.

castep_bin
: This file is essentially the same as `check` except it does not include the wave functions.

orbitals
: This file is very similar to `check` but stores wave functions of non-self-consistent field calculations, e.g. those from band structure and density of states calculations with fine sampling grids (*task* in *spectral*, *bandstructure*, and *optics*).
Activated by setting `write_orbitals : true` in the *param* file.


```{note}
Both `orbitals` and `check` files can be read with {py:func}`castepxbin.castep_bin.read_castep_bin` function.
The wave function will be read so make sure you have enough memory available.
At the moment, the packages does not support reading subsets of the wave function.
```
