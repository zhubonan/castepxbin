# {py:mod}`castepxbin.castep_bin`

```{py:module} castepxbin.castep_bin
```

```{autodoc2-docstring} castepxbin.castep_bin
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`FieldType <castepxbin.castep_bin.FieldType>`
  - ```{autodoc2-docstring} castepxbin.castep_bin.FieldType
    :summary:
    ```
* - {py:obj}`CompositeField <castepxbin.castep_bin.CompositeField>`
  - ```{autodoc2-docstring} castepxbin.castep_bin.CompositeField
    :summary:
    ```
* - {py:obj}`ScalarField <castepxbin.castep_bin.ScalarField>`
  - ```{autodoc2-docstring} castepxbin.castep_bin.ScalarField
    :summary:
    ```
* - {py:obj}`SkippedField <castepxbin.castep_bin.SkippedField>`
  - ```{autodoc2-docstring} castepxbin.castep_bin.SkippedField
    :summary:
    ```
* - {py:obj}`ArrayField <castepxbin.castep_bin.ArrayField>`
  - ```{autodoc2-docstring} castepxbin.castep_bin.ArrayField
    :summary:
    ```
* - {py:obj}`StrField <castepxbin.castep_bin.StrField>`
  - ```{autodoc2-docstring} castepxbin.castep_bin.StrField
    :summary:
    ```
* - {py:obj}`BoolField <castepxbin.castep_bin.BoolField>`
  - ```{autodoc2-docstring} castepxbin.castep_bin.BoolField
    :summary:
    ```
* - {py:obj}`StructuredField <castepxbin.castep_bin.StructuredField>`
  - ```{autodoc2-docstring} castepxbin.castep_bin.StructuredField
    :summary:
    ```
* - {py:obj}`EigenValueAndOccCompositeField <castepxbin.castep_bin.EigenValueAndOccCompositeField>`
  - ```{autodoc2-docstring} castepxbin.castep_bin.EigenValueAndOccCompositeField
    :summary:
    ```
* - {py:obj}`ChargeDensityField <castepxbin.castep_bin.ChargeDensityField>`
  - ```{autodoc2-docstring} castepxbin.castep_bin.ChargeDensityField
    :summary:
    ```
* - {py:obj}`WaveFunctionField <castepxbin.castep_bin.WaveFunctionField>`
  - ```{autodoc2-docstring} castepxbin.castep_bin.WaveFunctionField
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`read_castep_bin <castepxbin.castep_bin.read_castep_bin>`
  - ```{autodoc2-docstring} castepxbin.castep_bin.read_castep_bin
    :summary:
    ```
* - {py:obj}`_decode_records <castepxbin.castep_bin._decode_records>`
  - ```{autodoc2-docstring} castepxbin.castep_bin._decode_records
    :summary:
    ```
* - {py:obj}`_decode_composite <castepxbin.castep_bin._decode_composite>`
  - ```{autodoc2-docstring} castepxbin.castep_bin._decode_composite
    :summary:
    ```
* - {py:obj}`_generate_header_offset_map <castepxbin.castep_bin._generate_header_offset_map>`
  - ```{autodoc2-docstring} castepxbin.castep_bin._generate_header_offset_map
    :summary:
    ```
* - {py:obj}`_find_header_suffix <castepxbin.castep_bin._find_header_suffix>`
  - ```{autodoc2-docstring} castepxbin.castep_bin._find_header_suffix
    :summary:
    ```
* - {py:obj}`_read_record <castepxbin.castep_bin._read_record>`
  - ```{autodoc2-docstring} castepxbin.castep_bin._read_record
    :summary:
    ```
* - {py:obj}`_read_marker <castepxbin.castep_bin._read_marker>`
  - ```{autodoc2-docstring} castepxbin.castep_bin._read_marker
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`__all__ <castepxbin.castep_bin.__all__>`
  - ```{autodoc2-docstring} castepxbin.castep_bin.__all__
    :summary:
    ```
* - {py:obj}`TYPE_MAP <castepxbin.castep_bin.TYPE_MAP>`
  - ```{autodoc2-docstring} castepxbin.castep_bin.TYPE_MAP
    :summary:
    ```
* - {py:obj}`CASTEP_BIN_FIELD_SPEC <castepxbin.castep_bin.CASTEP_BIN_FIELD_SPEC>`
  - ```{autodoc2-docstring} castepxbin.castep_bin.CASTEP_BIN_FIELD_SPEC
    :summary:
    ```
* - {py:obj}`CASTEP_CHECK_FIELD_SPEC <castepxbin.castep_bin.CASTEP_CHECK_FIELD_SPEC>`
  - ```{autodoc2-docstring} castepxbin.castep_bin.CASTEP_CHECK_FIELD_SPEC
    :summary:
    ```
* - {py:obj}`CASTEP_BIN_FIELD_SHAPES <castepxbin.castep_bin.CASTEP_BIN_FIELD_SHAPES>`
  - ```{autodoc2-docstring} castepxbin.castep_bin.CASTEP_BIN_FIELD_SHAPES
    :summary:
    ```
````

### API

````{py:data} __all__
:canonical: castepxbin.castep_bin.__all__
:value: >
   ('read_castep_bin',)

```{autodoc2-docstring} castepxbin.castep_bin.__all__
```

````

````{py:data} TYPE_MAP
:canonical: castepxbin.castep_bin.TYPE_MAP
:value: >
   None

```{autodoc2-docstring} castepxbin.castep_bin.TYPE_MAP
```

````

`````{py:class} FieldType(name, dtype, endian='BIG')
:canonical: castepxbin.castep_bin.FieldType

```{autodoc2-docstring} castepxbin.castep_bin.FieldType
```

```{rubric} Initialization
```

```{autodoc2-docstring} castepxbin.castep_bin.FieldType.__init__
```

````{py:method} decode(fp, decoded=None, record_data=None)
:canonical: castepxbin.castep_bin.FieldType.decode

```{autodoc2-docstring} castepxbin.castep_bin.FieldType.decode
```

````

`````

````{py:class} CompositeField(fields: typing.List[castepxbin.castep_bin.FieldType])
:canonical: castepxbin.castep_bin.CompositeField

```{autodoc2-docstring} castepxbin.castep_bin.CompositeField
```

```{rubric} Initialization
```

```{autodoc2-docstring} castepxbin.castep_bin.CompositeField.__init__
```

````

`````{py:class} ScalarField(name, dtype, endian='BIG')
:canonical: castepxbin.castep_bin.ScalarField

Bases: {py:obj}`castepxbin.castep_bin.FieldType`

```{autodoc2-docstring} castepxbin.castep_bin.ScalarField
```

```{rubric} Initialization
```

```{autodoc2-docstring} castepxbin.castep_bin.ScalarField.__init__
```

````{py:method} decode(fp, decoded=None, record_data=None)
:canonical: castepxbin.castep_bin.ScalarField.decode

````

````{py:property} shape
:canonical: castepxbin.castep_bin.ScalarField.shape

```{autodoc2-docstring} castepxbin.castep_bin.ScalarField.shape
```

````

`````

`````{py:class} SkippedField()
:canonical: castepxbin.castep_bin.SkippedField

Bases: {py:obj}`castepxbin.castep_bin.FieldType`

```{autodoc2-docstring} castepxbin.castep_bin.SkippedField
```

```{rubric} Initialization
```

```{autodoc2-docstring} castepxbin.castep_bin.SkippedField.__init__
```

````{py:method} decode(fp, decoded=None, record_data=None)
:canonical: castepxbin.castep_bin.SkippedField.decode

```{autodoc2-docstring} castepxbin.castep_bin.SkippedField.decode
```

````

`````

`````{py:class} ArrayField(name, dtype, shape, endian='BIG')
:canonical: castepxbin.castep_bin.ArrayField

Bases: {py:obj}`castepxbin.castep_bin.ScalarField`

```{autodoc2-docstring} castepxbin.castep_bin.ArrayField
```

```{rubric} Initialization
```

```{autodoc2-docstring} castepxbin.castep_bin.ArrayField.__init__
```

````{py:property} shape
:canonical: castepxbin.castep_bin.ArrayField.shape

```{autodoc2-docstring} castepxbin.castep_bin.ArrayField.shape
```

````

````{py:method} resolve_shape(data)
:canonical: castepxbin.castep_bin.ArrayField.resolve_shape

```{autodoc2-docstring} castepxbin.castep_bin.ArrayField.resolve_shape
```

````

````{py:method} decode(fp, decoded=None, record_data=None)
:canonical: castepxbin.castep_bin.ArrayField.decode

```{autodoc2-docstring} castepxbin.castep_bin.ArrayField.decode
```

````

`````

`````{py:class} StrField(name, dtype, endian='BIG')
:canonical: castepxbin.castep_bin.StrField

Bases: {py:obj}`castepxbin.castep_bin.ScalarField`

```{autodoc2-docstring} castepxbin.castep_bin.StrField
```

```{rubric} Initialization
```

```{autodoc2-docstring} castepxbin.castep_bin.StrField.__init__
```

````{py:method} decode(fp, decoded=None, record_data=None)
:canonical: castepxbin.castep_bin.StrField.decode

````

`````

`````{py:class} BoolField(name, endian='BIG')
:canonical: castepxbin.castep_bin.BoolField

Bases: {py:obj}`castepxbin.castep_bin.ScalarField`

```{autodoc2-docstring} castepxbin.castep_bin.BoolField
```

```{rubric} Initialization
```

```{autodoc2-docstring} castepxbin.castep_bin.BoolField.__init__
```

````{py:method} decode(fp, decoded=None, record_data=None)
:canonical: castepxbin.castep_bin.BoolField.decode

````

`````

````{py:class} StructuredField(endian='BIG')
:canonical: castepxbin.castep_bin.StructuredField

```{autodoc2-docstring} castepxbin.castep_bin.StructuredField
```

```{rubric} Initialization
```

```{autodoc2-docstring} castepxbin.castep_bin.StructuredField.__init__
```

````

`````{py:class} EigenValueAndOccCompositeField(endian='BIG')
:canonical: castepxbin.castep_bin.EigenValueAndOccCompositeField

Bases: {py:obj}`castepxbin.castep_bin.StructuredField`

```{autodoc2-docstring} castepxbin.castep_bin.EigenValueAndOccCompositeField
```

```{rubric} Initialization
```

```{autodoc2-docstring} castepxbin.castep_bin.EigenValueAndOccCompositeField.__init__
```

````{py:method} decode(fp, decoded_data, record_data=None)
:canonical: castepxbin.castep_bin.EigenValueAndOccCompositeField.decode

```{autodoc2-docstring} castepxbin.castep_bin.EigenValueAndOccCompositeField.decode
```

````

`````

`````{py:class} ChargeDensityField(endian='BIG')
:canonical: castepxbin.castep_bin.ChargeDensityField

Bases: {py:obj}`castepxbin.castep_bin.StructuredField`

```{autodoc2-docstring} castepxbin.castep_bin.ChargeDensityField
```

```{rubric} Initialization
```

```{autodoc2-docstring} castepxbin.castep_bin.ChargeDensityField.__init__
```

````{py:method} decode(fp, decoded_data, record_data=None)
:canonical: castepxbin.castep_bin.ChargeDensityField.decode

```{autodoc2-docstring} castepxbin.castep_bin.ChargeDensityField.decode
```

````

`````

`````{py:class} WaveFunctionField(endian='BIG')
:canonical: castepxbin.castep_bin.WaveFunctionField

Bases: {py:obj}`castepxbin.castep_bin.StructuredField`

```{autodoc2-docstring} castepxbin.castep_bin.WaveFunctionField
```

```{rubric} Initialization
```

```{autodoc2-docstring} castepxbin.castep_bin.WaveFunctionField.__init__
```

````{py:attribute} STORE_COEFFS
:canonical: castepxbin.castep_bin.WaveFunctionField.STORE_COEFFS
:value: >
   False

```{autodoc2-docstring} castepxbin.castep_bin.WaveFunctionField.STORE_COEFFS
```

````

````{py:method} decode(fp, decoded_data, record_data=None)
:canonical: castepxbin.castep_bin.WaveFunctionField.decode
:staticmethod:

```{autodoc2-docstring} castepxbin.castep_bin.WaveFunctionField.decode
```

````

`````

````{py:data} CASTEP_BIN_FIELD_SPEC
:canonical: castepxbin.castep_bin.CASTEP_BIN_FIELD_SPEC
:value: >
   None

```{autodoc2-docstring} castepxbin.castep_bin.CASTEP_BIN_FIELD_SPEC
```

````

````{py:data} CASTEP_CHECK_FIELD_SPEC
:canonical: castepxbin.castep_bin.CASTEP_CHECK_FIELD_SPEC
:value: >
   None

```{autodoc2-docstring} castepxbin.castep_bin.CASTEP_CHECK_FIELD_SPEC
```

````

````{py:data} CASTEP_BIN_FIELD_SHAPES
:canonical: castepxbin.castep_bin.CASTEP_BIN_FIELD_SHAPES
:value: >
   None

```{autodoc2-docstring} castepxbin.castep_bin.CASTEP_BIN_FIELD_SHAPES
```

````

````{py:function} read_castep_bin(filename: typing.Union[str, pathlib.Path] = None, fileobj=None, records_to_extract: typing.Optional[typing.Collection[str]] = None, spec=None) -> typing.Dict[str, typing.Any]
:canonical: castepxbin.castep_bin.read_castep_bin

```{autodoc2-docstring} castepxbin.castep_bin.read_castep_bin
```
````

````{py:function} _decode_records(fp: io.BufferedReader, record_specs: typing.Tuple[castepxbin.castep_bin.FieldType], offset: int, decoded_data: dict = None) -> typing.Dict[str, typing.Any]
:canonical: castepxbin.castep_bin._decode_records

```{autodoc2-docstring} castepxbin.castep_bin._decode_records
```
````

````{py:function} _decode_composite(fp, record_spec)
:canonical: castepxbin.castep_bin._decode_composite

```{autodoc2-docstring} castepxbin.castep_bin._decode_composite
```
````

````{py:function} _generate_header_offset_map(fileobj) -> typing.Tuple[bool, typing.Dict[str, int]]
:canonical: castepxbin.castep_bin._generate_header_offset_map

```{autodoc2-docstring} castepxbin.castep_bin._generate_header_offset_map
```
````

````{py:function} _find_header_suffix(name, header_offset_map)
:canonical: castepxbin.castep_bin._find_header_suffix

```{autodoc2-docstring} castepxbin.castep_bin._find_header_suffix
```
````

````{py:function} _read_record(f: io.BufferedReader, seek_only: bool = False, record_marker_size: int = 4, read_data_smaller_than=512) -> typing.Tuple[typing.Optional[bytes], int]
:canonical: castepxbin.castep_bin._read_record

```{autodoc2-docstring} castepxbin.castep_bin._read_record
```
````

````{py:function} _read_marker(f: typing.Union[io.BufferedReader, bytes], record_marker_size: int = 4) -> int
:canonical: castepxbin.castep_bin._read_marker

```{autodoc2-docstring} castepxbin.castep_bin._read_marker
```
````
