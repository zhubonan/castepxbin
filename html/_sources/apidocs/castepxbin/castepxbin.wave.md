# {py:mod}`castepxbin.wave`

```{py:module} castepxbin.wave
```

```{autodoc2-docstring} castepxbin.wave
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`WaveFunction <castepxbin.wave.WaveFunction>`
  - ```{autodoc2-docstring} castepxbin.wave.WaveFunction
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`coords_to_indices <castepxbin.wave.coords_to_indices>`
  - ```{autodoc2-docstring} castepxbin.wave.coords_to_indices
    :summary:
    ```
* - {py:obj}`coeff_to_recip <castepxbin.wave.coeff_to_recip>`
  - ```{autodoc2-docstring} castepxbin.wave.coeff_to_recip
    :summary:
    ```
````

### API

````{py:function} coords_to_indices(grid_coords: numpy.ndarray, grid_size: numpy.ndarray)
:canonical: castepxbin.wave.coords_to_indices

```{autodoc2-docstring} castepxbin.wave.coords_to_indices
```
````

````{py:function} coeff_to_recip(coeffs: numpy.ndarray, nwaves_at_kp: numpy.ndarray, grid_coords: numpy.ndarray, ngx: int, ngy: int, ngz: int)
:canonical: castepxbin.wave.coeff_to_recip

```{autodoc2-docstring} castepxbin.wave.coeff_to_recip
```
````

`````{py:class} WaveFunction(coeffs, pw_grid_coords, mesh_size, nwaves_at_kp, kpts, recip_lattice, real_lattice, eigenvalues, occupancies, fermi_energy, data=None)
:canonical: castepxbin.wave.WaveFunction

```{autodoc2-docstring} castepxbin.wave.WaveFunction
```

```{rubric} Initialization
```

```{autodoc2-docstring} castepxbin.wave.WaveFunction.__init__
```

````{py:method} from_dict(full_data)
:canonical: castepxbin.wave.WaveFunction.from_dict
:classmethod:

```{autodoc2-docstring} castepxbin.wave.WaveFunction.from_dict
```

````

````{py:method} from_file(fname: typing.BinaryIO)
:canonical: castepxbin.wave.WaveFunction.from_file
:classmethod:

```{autodoc2-docstring} castepxbin.wave.WaveFunction.from_file
```

````

````{py:method} get_reciprocal_grid() -> numpy.ndarray
:canonical: castepxbin.wave.WaveFunction.get_reciprocal_grid

```{autodoc2-docstring} castepxbin.wave.WaveFunction.get_reciprocal_grid
```

````

````{py:method} get_plane_wave_coeffs(ispin=0, ik=0, ib=0, ispinor=0)
:canonical: castepxbin.wave.WaveFunction.get_plane_wave_coeffs

```{autodoc2-docstring} castepxbin.wave.WaveFunction.get_plane_wave_coeffs
```

````

````{py:method} get_gvectors(ik=0)
:canonical: castepxbin.wave.WaveFunction.get_gvectors

```{autodoc2-docstring} castepxbin.wave.WaveFunction.get_gvectors
```

````

````{py:method} get_gmesh_index(ik=0)
:canonical: castepxbin.wave.WaveFunction.get_gmesh_index

```{autodoc2-docstring} castepxbin.wave.WaveFunction.get_gmesh_index
```

````

````{py:method} get_kpoints_cart()
:canonical: castepxbin.wave.WaveFunction.get_kpoints_cart

```{autodoc2-docstring} castepxbin.wave.WaveFunction.get_kpoints_cart
```

````

`````
