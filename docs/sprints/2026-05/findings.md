# Findings from May 26th Code Sprint

This page documents the draft JSON Schema encoding rule that was developed for the JSON Schema generation with ShapeChange during the code sprint. It also documents results of the code sprint, as well as limitations, other aspects, and how to validate JSON data with the JSON Schemas developed during the code sprint.

## Draft JSON Schema Encoding Rule

The process of generating JSON Schemas with ShapeChange is based upon the conversion rules defined by the [Best Practice for OGC - UML to JSON Encoding Rules](https://docs.ogc.org/bp/24-017r1.html).

The encoding rule consists of the following requirements classes from the Best Practice document:

* http://www.opengis.net/spec/uml2json/1.0/req/core
* http://www.opengis.net/spec/uml2json/1.0/req/geojson-formats
* http://www.opengis.net/spec/uml2json/1.0/req/jsonfg
* http://www.opengis.net/spec/uml2json/1.0/req/by-reference-basic
* http://www.opengis.net/spec/uml2json/1.0/req/by-reference-link-object
* http://www.opengis.net/spec/uml2json/1.0/req/codelists-basic
* http://www.opengis.net/spec/uml2json/1.0/req/codelists-uri

The following subsections document further details on the JSON encoding.

### Schema $id

For the code sprint, the schema $id was chosen to follow the pattern `https://ext.iide.dev/schemas/geosciml/json/4.1/{actual json file}`. It is good practice to use the URL at which the schema file is published as identifier. For future work, the id should be changed to the publication URL.

### Reference of schema definitions

In the generated JSON Schema files, schema references use the anchor value as fragment identifier. It is possible to change this to a full JSON pointer (by setting ShapeChange JSON Schema target parameter `useAnchorsInLinksToGeneratedSchemaDefinitions` to false).

NOTE: Resolution of such fragment identifiers may depend upon the content type with which a JSON Schema file is published. For further details, see the last paragraph in https://docs.ogc.org/bp/24-017r1.html#jsonschema_req_core_definitionsschema

### Documentation

The definition (everything from the Notes field of a model element in Enterprise Architect) of a model element is encoded in the `description` member.


### External types

The GeoSciML application schemas depend upon a number of other schemas, primarily ISO schemas. The mappings for external types used in the GeoSciML schemas is defined in the ShapeChange configuration file [StandardMapEntries_JSON_for_GeoSciML.xml](https://github.com/opengeospatial/geosciml-json-code-sprint/blob/main/shapechange/config/StandardMapEntries_JSON_for_GeoSciML.xml).

For several external types (marked with `TBD` in the configuration file), a direct mapping to a standardized JSON Schema implementation was not found. For the code sprint, mappings were used that tried to suit the intent. However, finding and developing appropriate mappings requires future work. This is a limitation (documented further below).

NOTE: ISO 19107 geometry types are mapped to simple feature geometries. JSON-FG supports additional (non-simple) geometry types.


### Object identifier

The `id` member of a GeoJSON feature shall be used to encode the identifier of a GeoSciML feature.

NOTE: That is why the `identifier` properties of GeoSciMLLite feature types have not been encoded.

### Feature type

Each GeoSciML feature encoded in JSON shall have the feature type name within the `featureType` member (which is defined by JSON-FG, and also a required property in the generated JSON Schemas).


### Base schema for types with identity

The base schema for types with identity, i.e. types with stereotype «featuretype» and «type» is: https://schemas.opengis.net/json-fg/feature.json

From https://www.ogc.org/standards/json-fg/:

> GeoJSON is a very popular exchange format for feature data. GeoJSON is widely supported, including in most implementations of the OGC API – Features – Part 1: Core Standard. However, GeoJSON has intentional restrictions that prevent or limit its use in certain geospatial application contexts. For example, GeoJSON is restricted to using only WGS 84 coordinates in Longitude Latitude axis order, supports only the original Simple Features geometry types, and has no concept of classifying features according to their type.
> 
> The OGC Features and Geometries JSON (JSON-FG) Standard specifies GeoJSON extensions that provide standard ways to support these and other additional requirements. The JSON-FG Standardization goal is to focus on capabilities that may require some geospatial expertise, but that are useful in many applications. Edge cases are considered out-of-scope of JSON-FG.
> 
> Since JSON-FG specifies extensions to the GeoJSON RFC that still conform to the GeoJSON rules, valid JSON-FG features or feature collections are also valid GeoJSON features or feature collections.



### Primary geometry

The primary geometry is identified by setting tagged value `jsonPrimaryPlace` dynamically during execution of the ShapeChange workflow. For the code sprint, the tagged value was set to true for attributes named "shape" and "location". If the tagged value needs to be set for additional attributes, for one or more of the GeoSciML application schemas, then the relevant ShapeChange configurations can be extended accordingly.


### Primary temporal information

For the code sprint, no specific attributes were tagged to convey the primary temporal information of a feature. Further discussion is needed to identify relevant attributes. 


### Code lists

Code list valued properties use URIs as value. This reflects what GeoSciML experts communicated during the code sprint: _"CodeList values are encoded with URIs (https://docs.ogc.org/is/16-008/16-008.html#27). These potentially can be taken from different registries including ones that could be created by individual organisations if they needed their own values. The major ones are the CGI ones and the INSPIRE ones which are very similar."_

NOTE: Tagged value `codeList` has not been populated during the code sprint, since it was unclear which URLs to use for all the code lists defined in GeoSciML. If there is an authoritative set of code lists, then the according URLs can be added to the model on-the-fly by ShapeChange in the future, and represented with annotation `codeList` in the JSON Schema.

NOTE: DescriptionPurpose defines a number of codes. A code sprint participant said that _"It really is a fixed list at the model level (after long discussions...)"_. If code list DescriptionPurpose was modeled as (so agreed to be turned into) an enumeration, then using the "enum" keyword would be the correct encoding. However, a discussion is needed if this is another example of a code list where actual data may use different URIs (to custom code lists) - because if that is the case, then modeling the type as a code list would be the correct approach.


### What is not encoded

#### «voidable» stereotype

The JSON schemas generated for the code sprint do not support the 'voidable' concept, because that concept introduces a significant level of complexity, with questionable practical benefit. 

To fully support the concept in the JSON schema, voidable properties would all need to allow null as value. Furthermore, additional properties would likely be required, in order to convey the reason for a property having a null value. It should be discussed if this is a real requirement.

NOTE: The GeoSciMLLite application schema does not make use of the 'voidable' concept.

#### GeoSciMLLite attributes 

Attributes 'any' in GeoSciMLLite are not encoded, because the JSON schema definition for feature types allows additional properties. Thus, there is no need for an extension mechanism like the one introduced for the XML encoding of GeoSciML. Extensions can simply add the JSON members they need, and JSON Schema validation against the schema definition for a particular GeoSciML feature type would just ignore these additions (because no JSON Schema constraints are declared for the additional JSON members in that schema definition).

The 'identifier' property in GeoSciMLLite is also not encoded, because it is mapped to the 'id' member of a GeoJSON feature. In other words, the value of the identifier property shall be encoded in the id member.

#### GeoSciMLBasic types

Feature type GSML, as well as the union GSMLitem, are not encoded. They serve as containers for collections of GeoSciML features. That purpose can also be fulfilled by a [JSON-FG feature collection](https://schemas.opengis.net/json-fg/featurecollection.json). 

NOTE: If the provision of a GSML feature collection is deemed necessary, in order to define the `collectionType` attribute, then a suitable JSON Schema definition can be implemented in the future. 


### Feature references

References to features can be encoded inline or by reference. 

NOTE: The option for inline encoding was introduced primarily for the code sprint, for demonstration purposes.

By reference encoding uses link objects. That supports the "rel-as-link" profile from OGC API - Features - Part 5 / OGC API - Common - Part 3: Schemas.



## Results

* JSON Schema files have been created for all of the GeoSciML application schemas, and added to the [git repository for the GeoSciML JSON code sprint](https://github.com/opengeospatial/geosciml-json-code-sprint). However, note that limitations have been identified.
* ShapeChange configurations for automatically deriving the JSON Schema files are available in the repository.
* A number of examples with JSON encoded GeoSciML features and also feature collections have been created. A python script for validating the examples against the schemas, as well as automated GitHub actions to do so, were created.
  * Note that the examples contain the `conformsTo`-member, but without identifiers of JSON-FG conformance classes. That should be rectified in the future. 

## Limitations

### General

* Validation of a property value encoded in JSON, with the value having a complex type (i.e., being a JSON object or an array of JSON objects), only encompasses checking the JSON Schema constraints defined for that type. If the property value actually is a subtype of that type, then the constraints defined for that subtype are not checked. For further details, see section [Class Specialization and Property Ranges](https://docs.ogc.org/per/20-012.html#jsonschema_schemaconversionrules_types_inheritance_specialization) from the UML-to-GML Application Schema Pilot (UGAS-2020) Engineering Report.
  * Note that this limitation does not apply to GeoSciMLLite, because that application schema only uses simple and geometry types as property value types.
* For data published via OGC API Features, the schemas only support the "rel-as-link" profile for references. In the future, additional profiles can be added, especially "rel-as-uri". The "rel-as-link" profile was chosen for the code sprint, in order to reduce the level of complexity in the generated schemas.
* If a single object shall be validated, the URL to the schema definition against which to validate the object needs to be created, adding a fragment with either the anchor value defined for the schema definition (`#XYZ`) or the full JSON path to the definition (`#/$defs/XYZ`). During the code sprint, a wrapper schema was discussed, with a mechanism similar to that used in the `..._feature_collection.json` files, in order to automatically choose the right schema definition for validation, based upon the value of the featureType member in JSON encoded data. According schema constraints can be generated in the future - either in a separate wrapper schema file, or as part of the definitions schema file.
* The JSON Schema files were generated for each GeoSciML application schema individually. Thus, there is no JSON Schema with which one can validate a feature collection with feature types from multiple GeoSciML application schemas. In the future, such a feature collection schema file could be generated as well.


### Generated JSON Schemas

* All GeoSciML application schemas except GeoSciMLLite use external types (e.g. from Observations & Measurements). For several of those, no standardized JSON Schema implementation was found. That affects all of the generated JSON Schemas except the one for GeoSciMLLite.

## Other aspects

### Validation of JSON encoded objects based upon the value of their featureType-members

During the code sprint, participants discussed options for encoding a wrapper schema to automatically validate a JSON encoded feature against the right JSON Schema definition based upon the value of the featureType-member of the feature. The idea is that validation would then only need to use a single schema URI, rather than having to construct the schema URI with the right fragment identifier. Here is a brief summary on the pros and cons of using specific JSON Schema keywords and constructs for implementing such a wrapper schema:

* anyOf: 
  * Fully checks schema definitions until the first match is found. -> computing overhead
  * Can easily match the wrong schema definition if the given object satisfies the schema constraints (and especially taking into account that additional properties are allowed, so a schema definition with all optional properties is likely to match anything).
* oneOf:
  * Fully checks schema definitions until either the end of the definitions list is reached or two matching schemas were found. -> computing overhead
  * Same issue with matching the wrong schema definition as for anyOf.
* if-then-else:
  * Applies a particular schema definition based upon the featureType value of a given object.
  * Does not have the issues of computing overhead and matching wrong schema definition as the other two approaches.
  
NOTE: The feature collection schema files already apply the if-then-else-based approach.

  
## How to validate

This git repository has a validate.py script, with which examples are automatically validated.

For validating a JSON instance yourself, other JSON Schema validators can be used. An example is the online tool at https://www.jsonschemavalidator.net/.

Here is an example of a JSON Schema fragment for validating against the schema definition for feature type BoreholeView from GeoSciMLLite, with the schema file published (for the code sprint) on `https://ext.iide.dev` (note that interactive instruments will keep the files there at least until July 31, 2026 - they may be removed any time thereafter):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "https://ext.iide.dev/schemas/geosciml/json/4.1/geoscimlLite.json#/$defs/BoreholeView"
}
```