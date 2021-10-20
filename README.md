# castepxbin

## Overview

A collection of readers for binary output from [CASTEP](www.castep.org).

Available readers for:

- `pdos_bin`: Weights for computing the projected density of states.
- `castep_bin`: The compact checkpoint file contains internal data. High precision forces can be read from this file as the `geom` file is not written for singlepoint calculation. 
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

Simple import the function and pass the file path:

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

## Acknowledgement

The data structures of binary `pdos_bin`, `dome_bin`, `ome_bin`, `cst_esp` files are inferred from the code snippet
in the documentation of the open sourced [OptaDOS](https://github.com/optados-developers/optados) package for computing high quality DOS and other spectral properties using outputs from CASTEP.

## Contributors

- Bonan Zhu, University College London 
- Matthew Evans, UCLouvain/University of Cambridge