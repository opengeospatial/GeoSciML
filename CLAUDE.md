# GeoSciML JSON Code Sprint — project notes for Claude

## What this repo is

Development of a JSON encoding for GeoSciML 4.1, initially in support of the
May 2026 OGC Builder Days Code Sprint.  The main artefacts are JSON Schemas
(under `schemas/`) and conformant example instances (under `examples/`).

Reference GML 4.1 instances live in the sibling directory
`../schemas.opengis.net/gsml/4.1/instances/`.  Always read the relevant GML
file before writing a new example for a given type.

## Repository layout

```
schemas/json/4.1/           JSON Schema documents (one per feature family)
examples/json/4.1/
  <schema-name>/            Individual feature examples for that schema
  featurecollections/
    <schema-name>/          FeatureCollection examples for that schema
  validation_report.txt     Last recorded validate.py run
validate.py                 Validation script (see below)
venv/                       Python venv with jsonschema installed
.schema_cache/              Remote schema cache — auto-populated, git-ignored
```

Each schema file `schemas/json/4.1/<name>.json` has a companion example
directory `examples/json/4.1/<name>/` (individual features) and optionally
`examples/json/4.1/featurecollections/<name>/` (FeatureCollection documents).

## Validation

```bash
venv/bin/python validate.py
```

The script maps each example directory to its schema, fetches remote dependency
schemas (json-fg, SWE Common) on first run, caches them under `.schema_cache/`,
and exits with code 1 if any file fails.

Always run validation before committing and update the recorded report:

```bash
venv/bin/python validate.py > examples/json/4.1/validation_report.txt
```

## Adding a new example directory

1. Create `examples/json/4.1/<schema-name>/` for individual features, or
   `examples/json/4.1/featurecollections/<schema-name>/` for collections.
2. Register the directory in `validate.py` by adding an entry to `DIR_SCHEMA`:
   ```python
   EXAMPLES_DIR / "<schema-name>": f"{_BASE}/<schema-name>.json",
   EXAMPLES_DIR / "featurecollections/<schema-name>": f"{_BASE}/<schema-collection-name>.json",
   ```
   The validator automatically treats any path containing `featurecollections`
   as a collection (validated against the schema's top-level `$ref`); individual
   features are narrowed to the `$anchor` matching their `featureType`.
3. Run the validator to confirm the new directory is picked up.

## Writing a new example instance

### General structure (JSON-FG feature)

Every feature follows the JSON-FG feature structure:

```json
{
  "type": "Feature",
  "featureType": "<TypeName>",
  "id": "<unique-string>",
  "geometry": { <GeoJSON geometry in WGS84, or null> },
  "place":  { <geometry in local CRS — omit entirely if WGS84-only> },
  "coordRefSys": "<CRS URI — only when place is present, at Feature level>",
  "time": null,
  "properties": { ... }
}
```

- `featureType` must match a `$anchor` in the target schema.
- `geometry` uses WGS84 lon/lat.  `place` is only for non-WGS84 geometries;
  declare the CRS with `coordRefSys` **at the Feature level**, never inside the
  geometry object itself (json-fg prohibits it there).
- Purely descriptive features (e.g. GeologicUnit, GeologicEvent) typically have
  `geometry: null` and no `place`.

### SWE Common encoding

SWE Category, Quantity, and QuantityRange objects all require `type`,
`definition` (a URI), and `label` (a string).  Quantity and QuantityRange also
require `uom`.  Missing any of these causes a validation failure.

```json
{ "type": "Category",      "definition": "http://...", "label": "...", "value": "http://..." }
{ "type": "Quantity",      "definition": "http://...", "label": "...", "uom": {"code": "m"}, "value": 100.0 }
{ "type": "QuantityRange", "definition": "http://...", "label": "...", "uom": {"code": "%"}, "value": [5.0, 50.0] }
```

### Links vs inline objects

Properties that accept either a reference or an embedded object use
`oneOf [SCLinkObject, <Type>]`.  An SCLinkObject requires `href`:

```json
{ "href": "http://...", "title": "Human readable label" }
```

Use a link when the target is defined elsewhere; use an inline object when the
value is self-contained in the example.

### Lite schema specifics

All Lite properties are flat strings, numbers, or URIs — no nested SWE objects.
Properties suffixed `_uri` take a concept URI; the un-suffixed twin is a
human-readable string.

The Lite schema's `place` references `geometry-object.json` directly (no null
branch), so omit `place` entirely when the geometry is WGS84-only.  Add
`place` + `coordRefSys` (at Feature level) to show a non-WGS84 geometry.

### Feature collections

Homogeneous (single type): put `featureType` at the collection level.
Mixed: omit `featureType` from the collection; each feature carries its own.

## Vocabulary URIs

Use CGI / INSPIRE / ICS URIs consistently.  Common bases:

| Vocabulary | Base URI |
|---|---|
| CGI simple lithology | `http://resource.geosciml.org/classifier/cgi/simplelithology/` |
| CGI geologic unit type | `http://resource.geosciml.org/classifier/cgi/geologicunittype/` |
| CGI stratigraphic rank | `http://resource.geosciml.org/classifier/cgi/stratigraphicrank/` |
| CGI event process | `http://resource.geosciml.org/classifier/cgi/eventprocess/` |
| CGI fault type | `http://resource.geosciml.org/classifier/cgi/faulttype/` |
| CGI contact type | `http://resource.geosciml.org/classifier/cgi/contacttype/` |
| ICS chart (ages) | `http://resource.geosciml.org/classifier/ics/ischart/` |
| INSPIRE description purpose | `http://inspire.ec.europa.eu/codelist/DescriptionPurpose/` |
| INSPIRE composition part role | `http://inspire.ec.europa.eu/codelist/CompositionPartRoleValue/` |
