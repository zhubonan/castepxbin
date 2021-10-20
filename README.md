# castepxbin

## Overview

A collection of readers for binary output from [CASTEP](www.castep.org).
At the moment, there is only a reader for `pdos_dos` file available.
This file contains the weights of the eigenvalues on each projected orbitals,
which can be used to constructed projected density of states.

The code for reading `pdos_bin` files can be used as an example for implementing readers
of other files including: 

- `ome_bin`
- `dome_bin`
- `cst_esp`
- `elf`


## Installation

This package can be install using `pip`

```
pip install castepxbin
```

To install extra dependencies may be needed for testing:

```
pip install castepxbin[testing]
```

The two main dependencies are `numpy` and `scipy`. 
The optional `pymatgen` dependency is used for reordering orbitals.
Please note that the consistency of these labels for f orbitals has not been checked.

## Acknowledgement

The structure of the binary `pdos_bin` file is inferred from the code snippet
in the documentation of the open source [OptaDOS](https://github.com/optados-developers/optados) packages.