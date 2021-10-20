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

## Acknowledgement

The structure of the binary `pdos_bin`, `dome_bin`, `ome_bin`, `cst_esp` file is inferred from the code snippet
in the documentation of the open sourced [OptaDOS](https://github.com/optados-developers/optados) package for computing high quality DOS and other spectral properties using outputs from CASTEP.

## Contributors

Bonan Zhu, University College London, @zhubonan
Matthew Evans, UCLouvain/University of Cambridge, @ml-evans