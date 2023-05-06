# castepxbin

[Documentation](https://zhubonan.github.io/castepxbin/)
## Overview

A collection of readers for binary output from [CASTEP](http://www.castep.org).

Available readers for:

- `castep_bin`: The compact checkpoint file contains all internal data stored by CASTEP (excluding the wavefunction) and may be read for restarting. High precision forces can be read from this file for single point calculations, as the `geom` file not written.
- `check`: Same as `castep_bin` but includes wave function data (SCF kpoints).
- `orbitals`: Same as `check` but includes wave function data for sampled (none-SCF) k-points in spectral/bandstructure/optics tasks.
- `pdos_bin`: Weights for computing the projected density of states.
- `ome_bin`: Optical matrix elements from the *Spectral* task.
- `dome_bin`: Diagonal elements (band gradients) of the optical matrix from the *Spectral* task.
- `cst_ome`: Legacy format containing optical matrix elements from the *Optics* task.


To-dos:

- `cst_esp`: Electrostatic potentials?
- `elf`: Electron localsation function.
- More data from `castep_bin`/`check` files.


## Installation

This package can be install using `pip`

```
pip install castepxbin
```

To install extra dependencies may be needed for testing:

```
pip install castepxbin[testing]
```

Or directly from the GitHub repo:

```
pip install git+https://github.com/zhubonan/castepxbin.git
```

The two main dependencies are `numpy` and `scipy`.
The optional `pymatgen` dependency is used for naming the orbitals.
Please note that the consistency of these labels for the f orbitals has not been checked.

## Usage

Simply import the function and pass the file path. For the `castep_bin` reader, the example is shown below:

```python
In [1]: from castepxbin import read_castep_bin

In [2]: data = read_castep_bin("test_data/SiO2.castep_bin")

In [3]: data.keys()
Out[3]: dict_keys(['elec_temp', 'electronic_minimizer', 'nelectrons', 'nup', 'ndown', 'spin', 'charge', 'spin_treatment', 'num_ions_orig', 'max_ions_in_species_orig', 'real_lattice_orig', 'recip_lattice_orig', 'num_species_orig', 'num_ions_in_species_orig', 'ionic_positions', 'species_symbol_orig', 'num_ions', 'max_ions_in_species', 'real_lattice', 'recip_lattice', 'num_species', 'num_ions_in_species', 'species_symbol', 'nkpts', 'kpoints', 'kpoint_weights', 'found_ground_state_wavefunction', 'found_ground_state_density', 'total_energy', 'fermi_energy', 'nbands', 'nspins', 'occupancies', 'eigenvalues', 'kpoints_of_eigenvalues', 'ngx_fine', 'ngy_fine', 'ngz_fine', 'spin_density', 'charge_density', 'fermi_energy_second_spin', 'forces'])
```

Note that these readers should be considered as "low-level" as they corresponds to unprocessed Fortran data as it is. Further processes are often needed, such reordering the axes (Fortran arrays are column-major) and recasting into different `dtype`s.

Once exception is for the optical matrix element reader, where output array are converted into the "C" (row-major) ordering internally.

### Extending the `castep_bin` reader

At the moment, not all sections of the `castep_bin` is read (as there are too many!), but more contents can be added easily by including relevant sections in the `castepxbin.castep_bin.CASTEP_BIN_FIELD_SPEC` dictionary. The `read_castep_bin` function can accept such modified version instead of using the default one.

For example, suppose the binary field is written as such:

```fortran
header = 'MY_SECTION'
write(unit) header
write(unit) my_int    # An INTEGER(4)
write(unit) my_bool    # An LOGICAL type
write(unit) my_array    # An array of real numbers with size (3, nspecies, my_int)
header = 'END_MY_SECTION'
write(unit) header
```

The the following specifications can be added to read the section:

```python
my_spec = dict(CASTEP_BIN_FIELD_SPEC)
my_spec['MY_SECTION'] = (
        ScalarField('my_int', int),
        BoolField('my_bool'),
        ArrayField('my_array', float, shape=(3, 'nspecies', 'my_int'))
)
```

The value of `my_int` is unknown, but it is read before processing the `my_array` field.
This imples that the order of fields in `CASTEP_BIN_FIELD_SPEC` can be important, as certain array sizes are only available from other fields, such as the `nspecies` field above.
However, even if `nspecies` is not read previously, it can still be resolved by inspecting the length of the record.
This would not be possible if there are two unknown dimension sizes.

## Acknowledgement

The data structures of binary `pdos_bin`, `dome_bin`, `ome_bin`, files are inferred from the code snippet
in the documentation of the open sourced [OptaDOS](https://github.com/optados-developers/optados) package for computing high quality DOS and other spectral properties using outputs from CASTEP.

## Contributors

- Bonan Zhu, University College London
- Matthew Evans, UCLouvain/University of Cambridge
