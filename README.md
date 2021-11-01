# castepxbin

## Overview

A collection of readers for binary output from [CASTEP](http://www.castep.org).

Available readers for:

- `castep_bin`: The compact checkpoint file contains all internal data stored by CASTEP (excluding the wavefunction) and may be read for restarting. High precision forces can be read from this file for single point calculations, as the `geom` file not written.
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

Simply import the function and pass the file path:

```python
In [1]: from castepxbin import read_castep_bin

In [2]: read_castep_bin("test_data/SiO2.castep_bin")
Out[2]:
{'num_ions': 6,
 'max_ions_in_species': 4,
 'num_species': 2,
 'forces': array([[[ 3.32997451e-06, -1.00275146e-05],
         [ 7.92892004e-03,  3.53575656e-06],
         [ 3.36312207e-06,  0.00000000e+00],
         [-7.92912137e-03,  0.00000000e+00]],

        [[-7.93383055e-03,  1.66276581e-06],
         [ 5.54741296e-06,  7.35537943e-06],
         [ 7.92752830e-03,  0.00000000e+00],
         [-8.26331396e-06,  0.00000000e+00]],

        [[ 1.24161378e-06, -1.29568770e-06],
         [ 1.09647888e-06,  1.87501556e-06],
         [-3.54153006e-06,  0.00000000e+00],
         [ 6.24109535e-07,  0.00000000e+00]]])}
```

Note that these readers should be considered as "low-level" as they will read the data as it is in most cases, with the forces given above as one example. Further processes are often needed.

Once exception is the optical matrix element readers, where output array are converted into the "C" (row-major) ordering.

### Extending the `castep_bin` reader

At the moment, not all sections of the `castep_bin` is read (as there are too many!), but more contents can be added easity by including more keys the `castepxbin.castep_bin.CASTEP_BIN_FIELD_SPEC` dictionary, such an modified version can be passed to the `read_castep_bin` function.

For example, suppose some additional field is written as:

```fortran
header = 'MY_SECTION'
write(unit) header
write(unit) my_int    # An INTEGER(4)
write(unit) my_bool    # An LOGICAL type
write(unit) my_array    # An array of real numbers with size (3, nspecies)
header = 'END_MY_SECTION'
write(unit) header
```

The the following specification can be added:

```python
my_spec = dict(CASTEP_BIN_FIELD_SPEC)
my_spec['MY_SECTION'] = (
        ScalarField('my_int', int),
        BoolField('my_bool'),
        ArrayField('my_array', float, shape=(3, 'nspecies'))
)
```

The `nspecies` is unknown for now, but it can be read from other sections prior to processing the  'MY_SECTION' field.
This also means that the order of fields in `CASTEP_BIN_FIELD_SPEC` is important.
Not that for this special case, the `nspecies` can actually be resolve by inspecting the length of the record.
In fact, the value from `nspecies` can be inferred by reading the `my_array` field.
This will not be possible if there are two dimensions whose sizes are unknown.

## Acknowledgement

The data structures of binary `pdos_bin`, `dome_bin`, `ome_bin`, files are inferred from the code snippet
in the documentation of the open sourced [OptaDOS](https://github.com/optados-developers/optados) package for computing high quality DOS and other spectral properties using outputs from CASTEP.

## Contributors

- Bonan Zhu, University College London
- Matthew Evans, UCLouvain/University of Cambridge