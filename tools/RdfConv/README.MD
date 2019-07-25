# RDF converter (simple wrapper on Jena library)

## Example

`java -jar RdfConv.jar -i ..\..\instances\borehole.ttl -t JSON-LD > ..\..\instances\borehole.jsonld`

### Use a sparql query to extract triples 

(only supports CONSTRUCT, as it expect a model as a result)

`java -jar RdfConv.jar -i ..\..\instances\borehole.ttl -t JSON-LD -q bss000ecxq.sparql`

## Usage

to get usage instruction

`java -jar RdfConv.jar`

