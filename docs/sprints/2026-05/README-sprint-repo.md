# GeoSciML JSON Code Sprint

This repository is for the development of a JSON encoding for the Geoscience Markup Language (GeoSciML).

The repository was initially created in support of the May 2026 OGC Builder Days Code Sprint, but will continue to be used for GeoSciML activities in future code sprints.

## Candidate Standard

[Draft OGC Geoscience Markup Language (GeoSciML) - Part 1: Core](https://opengeospatial.github.io/geosciml-json-code-sprint/part1/)

[Draft OGC Geoscience Markup Language (GeoSciML) - Part 2: XML Encoding](https://opengeospatial.github.io/geosciml-json-code-sprint/part2/)

[DRAFT OGC Geoscience Markup Language (GeoSciML) - Part 3: JSON Encoding](https://opengeospatial.github.io/geosciml-json-code-sprint/part3/)

## Building the specification documents

The source files of the specification documents are in the folders part1_core, part2_xml, and part3_json.

To build the documents using metanorma, enter the folder containing document.adoc, and then run the following command.

```
metanorma compile --agree-to-terms -t ogc -x html document.adoc
```
If using metanorma through docker, then use this command instead:

```
docker run -v "$(pwd)":/metanorma -v ${HOME}/.fontist/fonts/:/config/fonts  metanorma/metanorma  metanorma compile --agree-to-terms -t ogc -x html,pdf document.adoc
```

## Updating GitHub Pages

Enter the folder containing document.adoc, and then run the following commands.

For part 3, for example:

```
cp ./document.pdf ../docs/part3
cp ./document.html ../docs/part3/index.html
```


## Notes from the May 2026 Code Sprint

The notes from the code sprint, as well as instructions for running ShapeChange can be found in [Findings_from_Code_Sprint_May26.md](Findings_from_Code_Sprint_May26.md)