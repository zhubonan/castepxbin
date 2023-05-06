# {py:mod}`castepxbin.pdos`

```{py:module} castepxbin.pdos
```

```{autodoc2-docstring} castepxbin.pdos
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`SpinEnum <castepxbin.pdos.SpinEnum>`
  - ```{autodoc2-docstring} castepxbin.pdos.SpinEnum
    :summary:
    ```
* - {py:obj}`OrbitalType <castepxbin.pdos.OrbitalType>`
  - ```{autodoc2-docstring} castepxbin.pdos.OrbitalType
    :summary:
    ```
* - {py:obj}`OrbitalEnum <castepxbin.pdos.OrbitalEnum>`
  - ```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`read_pdos_bin <castepxbin.pdos.read_pdos_bin>`
  - ```{autodoc2-docstring} castepxbin.pdos.read_pdos_bin
    :summary:
    ```
* - {py:obj}`reorder_pdos_data <castepxbin.pdos.reorder_pdos_data>`
  - ```{autodoc2-docstring} castepxbin.pdos.reorder_pdos_data
    :summary:
    ```
* - {py:obj}`compute_pdos <castepxbin.pdos.compute_pdos>`
  - ```{autodoc2-docstring} castepxbin.pdos.compute_pdos
    :summary:
    ```
* - {py:obj}`_merge_weights <castepxbin.pdos._merge_weights>`
  - ```{autodoc2-docstring} castepxbin.pdos._merge_weights
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`__all__ <castepxbin.pdos.__all__>`
  - ```{autodoc2-docstring} castepxbin.pdos.__all__
    :summary:
    ```
````

### API

````{py:data} __all__
:canonical: castepxbin.pdos.__all__
:value: >
   ['read_pdos_bin', 'compute_pdos', 'reorder_pdos_data']

```{autodoc2-docstring} castepxbin.pdos.__all__
```

````

`````{py:class} SpinEnum
:canonical: castepxbin.pdos.SpinEnum

Bases: {py:obj}`enum.Enum`

```{autodoc2-docstring} castepxbin.pdos.SpinEnum
```

````{py:method} __int__()
:canonical: castepxbin.pdos.SpinEnum.__int__

```{autodoc2-docstring} castepxbin.pdos.SpinEnum.__int__
```

````

````{py:method} __float__()
:canonical: castepxbin.pdos.SpinEnum.__float__

```{autodoc2-docstring} castepxbin.pdos.SpinEnum.__float__
```

````

````{py:method} __str__()
:canonical: castepxbin.pdos.SpinEnum.__str__

````

`````

`````{py:class} OrbitalType
:canonical: castepxbin.pdos.OrbitalType

Bases: {py:obj}`enum.Enum`

```{autodoc2-docstring} castepxbin.pdos.OrbitalType
```

````{py:attribute} s
:canonical: castepxbin.pdos.OrbitalType.s
:value: >
   0

```{autodoc2-docstring} castepxbin.pdos.OrbitalType.s
```

````

````{py:attribute} p
:canonical: castepxbin.pdos.OrbitalType.p
:value: >
   1

```{autodoc2-docstring} castepxbin.pdos.OrbitalType.p
```

````

````{py:attribute} d
:canonical: castepxbin.pdos.OrbitalType.d
:value: >
   2

```{autodoc2-docstring} castepxbin.pdos.OrbitalType.d
```

````

````{py:attribute} f
:canonical: castepxbin.pdos.OrbitalType.f
:value: >
   3

```{autodoc2-docstring} castepxbin.pdos.OrbitalType.f
```

````

````{py:method} __str__()
:canonical: castepxbin.pdos.OrbitalType.__str__

````

`````

`````{py:class} OrbitalEnum
:canonical: castepxbin.pdos.OrbitalEnum

Bases: {py:obj}`enum.Enum`

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum
```

````{py:attribute} s
:canonical: castepxbin.pdos.OrbitalEnum.s
:value: >
   'S'

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum.s
```

````

````{py:attribute} px
:canonical: castepxbin.pdos.OrbitalEnum.px
:value: >
   'Px'

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum.px
```

````

````{py:attribute} py
:canonical: castepxbin.pdos.OrbitalEnum.py
:value: >
   'Py'

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum.py
```

````

````{py:attribute} pz
:canonical: castepxbin.pdos.OrbitalEnum.pz
:value: >
   'Pz'

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum.pz
```

````

````{py:attribute} dxy
:canonical: castepxbin.pdos.OrbitalEnum.dxy
:value: >
   'Dxy'

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum.dxy
```

````

````{py:attribute} dyz
:canonical: castepxbin.pdos.OrbitalEnum.dyz
:value: >
   'Dzy'

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum.dyz
```

````

````{py:attribute} dz2
:canonical: castepxbin.pdos.OrbitalEnum.dz2
:value: >
   'Dzz'

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum.dz2
```

````

````{py:attribute} dxz
:canonical: castepxbin.pdos.OrbitalEnum.dxz
:value: >
   'Dzx'

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum.dxz
```

````

````{py:attribute} dx2
:canonical: castepxbin.pdos.OrbitalEnum.dx2
:value: >
   'Dxx-yy'

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum.dx2
```

````

````{py:attribute} f_xxx
:canonical: castepxbin.pdos.OrbitalEnum.f_xxx
:value: >
   'Fxxx'

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum.f_xxx
```

````

````{py:attribute} f_yyy
:canonical: castepxbin.pdos.OrbitalEnum.f_yyy
:value: >
   'Fyyy'

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum.f_yyy
```

````

````{py:attribute} f_zzz
:canonical: castepxbin.pdos.OrbitalEnum.f_zzz
:value: >
   'Fzzz'

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum.f_zzz
```

````

````{py:attribute} f_xyz
:canonical: castepxbin.pdos.OrbitalEnum.f_xyz
:value: >
   'Fxyz'

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum.f_xyz
```

````

````{py:attribute} f_z_xx_yy
:canonical: castepxbin.pdos.OrbitalEnum.f_z_xx_yy
:value: >
   'Fz(xx-yy)'

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum.f_z_xx_yy
```

````

````{py:attribute} f_y_zz_xx
:canonical: castepxbin.pdos.OrbitalEnum.f_y_zz_xx
:value: >
   'Fy(zz-xx)'

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum.f_y_zz_xx
```

````

````{py:attribute} f_x_yy_zz
:canonical: castepxbin.pdos.OrbitalEnum.f_x_yy_zz
:value: >
   'Fx(yy-zz)'

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum.f_x_yy_zz
```

````

````{py:method} __int__()
:canonical: castepxbin.pdos.OrbitalEnum.__int__

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum.__int__
```

````

````{py:method} __str__()
:canonical: castepxbin.pdos.OrbitalEnum.__str__

````

````{py:property} orbital_type
:canonical: castepxbin.pdos.OrbitalEnum.orbital_type
:type: castepxbin.pdos.OrbitalType

```{autodoc2-docstring} castepxbin.pdos.OrbitalEnum.orbital_type
```

````

`````

````{py:function} read_pdos_bin(filename: typing.Union[str, typing.BinaryIO], endian='big') -> typing.Dict[str, typing.Any]
:canonical: castepxbin.pdos.read_pdos_bin

```{autodoc2-docstring} castepxbin.pdos.read_pdos_bin
```
````

````{py:function} reorder_pdos_data(input_items: typing.Dict[str, typing.Any], pymatgen_labels: bool = True, use_string_as_keys: bool = False) -> dict
:canonical: castepxbin.pdos.reorder_pdos_data

```{autodoc2-docstring} castepxbin.pdos.reorder_pdos_data
```
````

````{py:function} compute_pdos(pdos_bin: str, eigenvalues: typing.Dict[castepxbin.pdos.SpinEnum, numpy.ndarray], kpoints_weights: numpy.ndarray, bins: numpy.ndarray) -> typing.Dict[str, typing.Any]
:canonical: castepxbin.pdos.compute_pdos

```{autodoc2-docstring} castepxbin.pdos.compute_pdos
```
````

````{py:function} _merge_weights(spin_d1: dict, spin_d2: dict) -> dict
:canonical: castepxbin.pdos._merge_weights

```{autodoc2-docstring} castepxbin.pdos._merge_weights
```
````
