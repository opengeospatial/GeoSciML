# Notes on implementing GeoSciML in OWL

How to connect CGI vocabularies to GeoSciML OWL

Implemented each vocab in separate ontology. Build one ontology to import all the vocabularies (aggregator). A geosciml instance imports the aggregator.

In the GeoSciML owl, the vocab properties are typed with a class that is the top category for the intended vocabulary. The GeoSciML ontology only includes these top-level 'hook' classes, the vocabulary ontologies include the extensions.

## Definition of property
    <owl:ObjectProperty rdf:about="&CGI_Lith;ConsolidationDegree">
        <rdf:type rdf:resource="&owl;FunctionalProperty"/>
        <rdfs:label>consolidation degree</rdfs:label>
        <rdfs:range rdf:resource="&CGI_Lith;AnyConsolidationDegree"/>
        <rdfs:domain rdf:resource="&CGI_Lith;rock_material"/>
    </owl:ObjectProperty>
	
	
	OR
	
	<owl:ObjectProperty rdf:about="&CGI_Lith;hasConsolidationDegree">
        <rdf:type rdf:resource="&owl;FunctionalProperty"/>
        <rdfs:label>consolidation degree</rdfs:label>
        <rdfs:range rdf:resource="&CGI_Lith;ConsolidationDegree"/>
        <rdfs:domain rdf:resource="&CGI_Lith;rock_material"/>
    </owl:ObjectProperty>
	
	
## Definition of a rockMaterial class

<owl:Class rdf:about="&CGI_Lith;alkali_feldspar_granite">
        <rdfs:label>alkali feldspar granite</rdfs:label>
        <owl:equivalentClass>
            <owl:Class>
                <owl:intersectionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&CGI_Lith;rock_material"/>
                    <owl:Restriction>
                        <owl:onProperty rdf:resource="&CGI_Lith;ChemCat"/>
                        <owl:allValuesFrom rdf:resource="&CGI_Lith;acidic"/>
                    </owl:Restriction>
                    <owl:Restriction>
                        <owl:onProperty rdf:resource="&CGI_Lith;hasConsolidationDegree"/>
                        <owl:allValuesFrom rdf:resource="&CGI_Lith;consolidated"/>
                    </owl:Restriction>
					.....
	
## Vocabulary construction:	
    <owl:Class rdf:about="http://resource.geosciml.org/classifier/cgi/lithOntology/AnyConsolDegree">
        <rdfs:label>any consolidation degree</rdfs:label>
    </owl:Class>
	<owl:Class rdf:about="http://resource.geosciml.org/classifier/cgi/lithOntology/consolidated">
        <rdfs:subClassOf rdf:resource="http://resource.geosciml.org/classifier/cgi/lithOntology/AnyConsolDegree"/>
        <rdfs:label xml:lang="en">consolidated</rdfs:label>
    </owl:Class>	
    <owl:Class rdf:about="http://resource.geosciml.org/classifier/cgi/lithOntology/unconsolidated">
        <rdfs:subClassOf rdf:resource="http://resource.geosciml.org/classifier/cgi/lithOntology/AnyConsolDegree"/>
        <rdfs:label xml:lang="en">unconsolidated</rdfs:label>
    </owl:Class>	
					
					
# NOTES:	
					
MineralTerm, LithologyTerm and the '...Type' properties in the UML are classifiers; these would get implemetned in OWL as subclasses. Mark the UML with stereotypes in the 3.2 version to help automate the shapechange transformation. The CGI vocabularies for these subclasses are not encoded into the GeoSciML OWL model, but as imports that extend the base classes in the OWL.  In modular specification terms, define different conformance classes: conforms to model; 2) uses CGI vocabulary models.


# Process steps

* Annotate UML 3.2 diagram for soft types add stereotypes to flag properties that need special handling.
* Follow packaging in 3.2. model.
* Separate namespaces for each vocabulary
* get shapechange cofig for existing
* generate vocabularies from SKOS
* Look for where other ontologies plug in (SSN, SOSA, GEoTime, Metadata)
* For now leave Borehole and LaboratoryAnalysis-Specimen out
* Check with ELFIE team for how to deal with geometry/shapechange

* Evaluate what we have. 

* implement--repository, sparql endpoint, paper


