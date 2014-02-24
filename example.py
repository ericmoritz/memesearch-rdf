"""
This is an example of consuming an RDF graph using Python.
It is quite simple because we can use SPARQL with rdflib
"""

from rdflib import Graph
from rdflib_jsonld.parser import to_rdf
import json
from pprint import pprint
import requests


def query_collection(g):
    r = g.query("""
    PREFIX meme: <http://memegenerator.net/vocab/meme#>
    PREFIX schema: <http://schema.org/>
    PREFIX hydra: <http://www.w3.org/ns/hydra/core#>

    SELECT ?id
    WHERE {
       ?members hydra:members ?id
    }""")
    return list(r)


def all_meme_collection(g):
    """
    Return a Hydra collection in JSON-LD of all meme:Meme objects in the graph.
    """

    r = g.query("""
    PREFIX meme: <http://memegenerator.net/vocab/meme#>
    PREFIX schema: <http://schema.org/>

    SELECT ?id ?image ?bottomText ?topText
    WHERE {
    ?id rdf:type meme:Meme ;
    schema:image ?image ;
    meme:topText ?topText ;
    meme:bottomText ?bottomText .
    }""")
    return {
        "@context": {
            "hydra": "http://www.w3.org/ns/hydra/core#",
            "members": "hydra:members",
        },
        "@id": "memeListing",
        "@type": "hydra:Collection",
        "members": [
            {
                "@context": {
                    "schema": "http://schema.org/", 
                    "meme": "http://memegenerator.net/vocab/meme#",
                    "image": "schema:image",
                    "topText": "meme:topText",
                    "bottomText": "meme:bottomText"
                },
                "@type": "meme:Meme",
                "@id": str(iri), 
                "image": str(image), 
                "topText": str(topText),
                "bottomText": str(bottomText)
            }
            for iri, image, topText, bottomText in r
        ]
    }


# Create a graph from the meme.html microdata
g = Graph().parse("./meme.html", format="microdata")

# extract all the memes on the page
collection = all_meme_collection(g)
pprint(collection)


    
