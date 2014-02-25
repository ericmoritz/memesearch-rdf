from gevent.monkey import patch_all
patch_all()

from pyquery import PyQuery
import grequests
from rdflib import Graph, Namespace, URIRef, Literal
import json
import re
from pprint import pprint
from urlparse import urljoin
from itertools import izip, imap
import logging
from datetime import datetime
from urllib import quote
import os

log = logging.getLogger("memescraper")

rdfNS = Namespace("http://w3.org/TR/1999/PR-rdf-syntax-19990105#")
memeNS = Namespace("http://memesearch.example.com/vocab/meme#")
schemaNS = Namespace("http://schema.org/")

memeDataSrcRe = re.compile(r"var memeData=(.+)")

###===================================================================
### Utilities
###===================================================================
def _urljoin(base_url, url):
    return quote(
        urljoin(base_url, url, allow_fragments=True),
        safe=":/"
    )


def download_all(url_list):
    return izip(
        url_list,
        grequests.map(imap(grequests.get, url_list))
    )


def add_statements(g, generator):
    def _make_statement(g, statement):
        g.add(statement)
        return g
    return reduce(_make_statement, generator, g)
        


###===================================================================
### Statement Generators
###===================================================================

def diylol_recent_statements(base_url, html_src):
    """
    Yields statements about meme:MemeKind objects
    on http://diylol.com/memes/featured/recent
    """
    pq = PyQuery(html_src)
    for script in pq.find("script"):
        cdata = script.text or ""
        match = memeDataSrcRe.search(cdata)
        if match:
            data = json.loads(match.group(1))
            for obj in data:
                iri = URIRef(_urljoin(base_url, obj['url']))
                thumb = URIRef(_urljoin(base_url, obj['img_src']))

                yield (iri, rdfNS['type'], memeNS.MemeKind, )
                yield (iri, rdfNS['type'], schemaNS.Thing, )
                yield (iri, schemaNS.url, iri, )
                yield (iri, schemaNS.title, Literal(obj['title']), )
                yield (iri, schemaNS.thumbnailUrl, thumb)


def recent_meme_statements(meme_kind_iri, base_url, html_src):
    """
    Yields statements about meme:Meme objects
    found on the recent meme page
    """
    pq = PyQuery(html_src)
    for div in pq("div.img-w-txt-headers"):
        # extract data
        thumb_anchor = PyQuery(div.find('a[@class="thumbnail"]'))
        image_url = _urljoin(base_url, thumb_anchor.find("img").attr("src"))
        topText = div.find('*[@class="post_line1"]').text
        bottomText = div.find('*[@class="post_line1"]').text
        href = _urljoin(base_url, thumb_anchor.attr("href"))

        iri = URIRef(href)
        yield (iri, rdfNS['type'], memeNS.Meme, )
        yield (iri, rdfNS['type'], schemaNS.Thing, )
        yield (iri, schemaNS.url, iri, )
        yield (iri, schemaNS.image, URIRef(image_url), )
        yield (iri, memeNS.hasMemeKind, meme_kind_iri, )
        yield (iri, memeNS.bottomText, Literal(bottomText), )
        yield (iri, memeNS.topText, Literal(topText), )


def save(g):
    filename = "data/{dt}.memes.n3".format(dt=datetime.now().isoformat(), )
    with open(filename, "w") as fh:
        log.info(
            "saving data to <file://{filename}>".format(
                filename=os.path.abspath(filename)
            )
        )
        print g.serialize(format="n3")


def main():
    logging.basicConfig(level=logging.INFO)

    g = Graph()
    g = reduce(
        add_statements,
        (
            diylol_recent_statements(uri, response.content)
            for (uri, response) in download_all([u"http://diylol.com/memes/featured/recent"])
        ),
        g
    )

    r = g.query("""
    PREFIX rdf: <http://w3.org/TR/1999/PR-rdf-syntax-19990105#>
    PREFIX meme: <http://memesearch.example.com/vocab/meme#>

    SELECT ?iri
    WHERE {
        ?iri rdf:type meme:MemeKind .
    }
    """)
    g = reduce(
        add_statements,
        (
            recent_meme_statements(meme_kind_iri, url, response.content)
            for (url, response) in download_all(
                    (iri.toPython() for (iri, ) in r)
            )
        ),
        g
    )

    save(g)

        
if __name__ == '__main__':
    main()
