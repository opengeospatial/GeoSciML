# GeoJson encoding for GeoSciML 4.2

This repository proposes  options for an encoding of GeoSciML in GeoJson.  There are several approaches that can be considered when designing a an encodind.  The modular specification provides different modules that can be reused an extended.  GeoSciML lite is itself an extension of GeoSciML and at this point we can base the encoding on GeoSciML or start over from the conceptual model.  The question will come down to "it's a GeoJson encoding of what ?".

In 8.9.2.5, it is written

Some community (sic) might create a profile of this requirements class and add more constraints, such as mandatory resolution of the URI to one or more resources and impose mandatory mime-types (GeoSciML/XML or GeoSciML/GeoJSON).


Some early work by BRGM : https://github.com/INSPIRE-MIF/2017.2/issues/34

## Why

### OGC API friendly

OGC API does not impose any format, but JSON is the format use to interact with the API and certainly expected as one of format to get the spatial data.  Because JSON is automatically parse and injested by any javascript compiler/interpreter, it is favored by web developer who don't need to address serialization / deserialization. It has caveats : it quite limits the format to JSON - which is the serialization of a javascript plain object

As a quick win, it was agreed to encoding GeoSciML lite, because of it simplicity and expected 1:1 mapping

GeoJSON specification : https://tools.ietf.org/html/rfc7946

A GeoJSON (?) encoding has already been published by BRGM (others ?) based on GeoServer implementation 

   * [Geologic Unit](geologicunit.adoc)
   * [Borehole](borehole.adoc) 



## Issues

Things that prevent us to be a strict encoding of GML and justify to go back to "conceptual".  In other words, 

### Geometry property

GeoSciML lite expects the geometry to be in a field called "shape", but GeoJSON already imposes "geometry".  Spatial query would technically target a different field depending of the encoding, but the spatial field is often "implicit" as the basic GML Level 0 model assume there is one and only on geometry per feature.

So "lite" has a extra redundant property

(Issue: #)

### Properties

Section 3.2 states that "properties" can be any GeoJSON object (or null)

"A Feature object has a member with the name "properties".  The value of the properties member is an object (any JSON object or a JSON null value)."

GeoSciML lite encodes everything as literal values (or simple types, such as numerical and string - except the geometry, even if the content type is really of a type that has specific encoding, such as URI.  It is not clear what is "valid".

This is valid according to GeoJSON validator, but is not strickly equivalent to GeoSciML lite (there is an extra bit of information)

```json
"representativeOlderAge_uri": {
        "href":"http://www.opengis.net/def/nil/OGC/0/unknown",
        "title":"unknown"
        }
```

Also, in GeoSciML lite, we accept list of URL in a single field

```json
"representativeLithology_uri": "http://inspire.ec.europa.eu/codelist/LithologyValue/clasticSediment,http://inspire.ec.europa.eu/codelist/LithologyValue/limestone",
```

(which greatly limits queryability BTW)

Do we allow arrays (similar argument)

```json
"representativeLithology_uri": ["http://inspire.ec.europa.eu/codelist/LithologyValue/clasticSediment","http://inspire.ec.europa.eu/codelist/LithologyValue/limestone"],
```

This is an important consideration since providers can insert any of those non-strickly character form in the "any" zone, leading to mixed pattern (maybe an argument to start from scratch for *both* new XML GML 3.2 and GeoJSON encodings) 

(Issue: #)

### id

We need to clarify what "id" is supposed to mean.  Is it the gml:id (local transitive id of the source) or the global id (ie, its URI).  It suspect it's the first, therefore, we need a way to define the second.

### duplicate properties

JSON has no concept of namespace.   JSON-LD does, which means that we need to deal with the duplicate identifier issue. 

(Issue: #)

### validation

https://geojsonlint.com/ can validate geojson, but will just test spec requirements for any GeoJSON, not for "GeoSciML".  What is the JSON validation strategy here ?

# Proposals 

   * `any` should be foreign members ? (See section 3.1.6 of GeoJSON) not sure what is the gain expect telling the user it's provider specfic ?
   * the CRS attribute (that was introduced in GJ2008 and then removed should be implemented as a profile)


