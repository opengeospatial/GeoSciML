# GeoSciML

GeoSciML is the OGC and IUGS-CGI standard for geological data: geologic units, contacts, faults, earth materials, boreholes and geological time. It gives that data shared meaning through a conceptual model and persistent vocabularies.

- **Published standard:** GeoSciML 4.1 ([OGC 16-008](https://docs.ogc.org/is/16-008/16-008.html), [standard page](https://www.ogc.org/standards/geosciml/))
- **In development:** GeoSciML 5, starting from the May 2026 JSON code sprint

## Status

| Part | Folder | Status |
| --- | --- | --- |
| Part 1: Conceptual model | `core/` | Draft (v5) |
| Part 2: XML encoding | `xml/` | Draft (v5); 4.1 XML schemas remain at [schemas.opengis.net/gsml](https://schemas.opengis.net/gsml/) |
| Part 3: JSON encoding (JSON-FG) | `json/` | Draft (v5); schemas and examples for every 4.1 package |
| Part 4: Earth Resources (EarthResourceML) | — | Proposed |
| GeoSciML 4.1 in Metanorma | `releases/4.1/` | Conversion of OGC 16-008 for docs.ogc.org |

The drafts are working documents and are not yet OGC standards.

## Repository layout

```text
model/       UML model (Enterprise Architect) and ShapeChange configurations
core/        Part 1 source (Metanorma)
xml/         Part 2 source
json/        Part 3 source, JSON Schemas and examples
releases/    Published versions kept buildable (4.1)
docs/        Background material, including the 2026 code sprint
archive/     Superseded material kept for history (3.2 OWL, GeoJSON notes, old tools)
tools/       Validation scripts
```

## Validate the JSON examples

Requires Python 3 and internet access (remote schemas are cached in `.schema_cache/`).

```bash
python3 -m venv .venv
.venv/bin/pip install -r tools/validate/requirements.txt
.venv/bin/python tools/validate/validate.py
```

## Build a document locally

From a part's `standard/` folder, using the Metanorma Docker image:

```bash
docker run -v "$(pwd)":/metanorma metanorma/metanorma \
  metanorma compile --agree-to-terms -t ogc -x html document.adoc
```

`-x html` is quickest; add `pdf` for a PDF (it needs more memory).

## Vocabularies

GeoSciML and EarthResourceML vocabularies are published at `http://resource.geosciml.org/` and maintained in [GeoscienceAustralia/cgi-vocabs](https://github.com/GeoscienceAustralia/cgi-vocabs). Geological time is maintained by the ICS at [stratigraphy.org/data-models](https://stratigraphy.org/data-models).

## History

In November 2026 this repository absorbed the [geosciml-json-code-sprint](https://github.com/opengeospatial/geosciml-json-code-sprint) repository and the CGI-IUGS 4.1 Metanorma conversion, with their commit histories preserved. Built documents were removed from the imported history, and Metanorma caches are no longer tracked.

## Contributing

Raise an issue or open a pull request. GeoSciML is maintained by the OGC GeoSciML Standards Working Group with the IUGS Commission for the Management and Application of Geoscience Information (CGI).