from flask import Flask, Response
import json
app = Flask(__name__)
###===================================================================
### Data access functions
###===================================================================
MEME_DB = {
    "bn0x9np": {
        "@id": "/meme/bn0x9np",
        "@type": ["hydra:Link", "meme:MemeDetailPage"],
        "name": "Its an unbearably small world",
        "image": "http://i.imgur.com/ej3mFrZb.jpg",
        "url": "/meme/bn0x9np",
    },
    "DiaODFK": {
        "@id": "/meme/DiaODFK",
        "@type": ["hydra:Link", "meme:MemeDetailPage"],
        "name": "I shall not pass.",
        "image": "http://i.imgur.com/DiaODFKb.jpg",
        "url": "/meme//DiaODFK"
    }
}
class DB(object):
    def search(self, query):
        """
        Returns a list of meme:Meme objects
        """
        return [MEME_DB['bn0x9np'], MEME_DB['DiaODFK']]


    def recent(self):
        """
        Returns a list of recent meme:Meme objects
        """
        return [MEME_DB['bn0x9np'], MEME_DB['DiaODFK']]

    def meme(self, index):
        return MEME_DB.get(index)
        

###===================================================================
### Utilities
###===================================================================

def _json_response(data):
    return Response(
        json.dumps(
            _merge_dict(_web_page(), data)
        ),
        content_type = "application/json",
    )


def _merge_dict(base, extension):
    return dict(base, **extension)


###===================================================================
### Base objects
###===================================================================
def _web_page():
    return {
        "@context": "/meme.jsonld",
        "homepage": "/",
        "searchLink": {
            "@type": "IriTemplate",
            "template": "/meme-search{?q}",
            "mappings": [
                {
                    "@type": "IriTemplateMapping", 
                    "variable": "q",
                    "proprety": "hydra:freetextQuery",
                    "required": True
                }
            ]
        },
    }

###===================================================================
### Resources
###===================================================================

###-------------------------------------------------------------------
### meme.jsonld resource
###-------------------------------------------------------------------
@app.route("/meme.jsonld")
def meme_jsonld():
    return Response(
        open("./meme.jsonld").read(),
        content_type = "application/json"
    )
        
###-------------------------------------------------------------------
### meme:SearchResultsPage
###-------------------------------------------------------------------
@app.route("/meme-search")
def meme_search():
    query = ""
    return _json_response(
            _search_collection(query)
    )


def _search_collection(query):
    """
    Returns a meme:SearchResultPage
    """
    return {
        "@type": "meme:SearchResultPage",
        "member": _search_member(query)
    }


def _search_member(query):
    """
    Returns a list of meme:Meme objects
    """
    # TODO: do the full text search
    return DB().search(query)


###-------------------------------------------------------------------
### Meme Detail Page
###-------------------------------------------------------------------
@app.route("/meme/<index>")
def meme(index):
    # TODO: do lookup
    return _json_response(_meme_resource(index))
        
def _meme_resource(index):
    """
    Returns a meme:MemeDetailPage
    """
    meme = DB().meme(index)
    if meme is not None:
        return meme


###-------------------------------------------------------------------
### meme:IndexPage
###-------------------------------------------------------------------
@app.route("/")
def index():
    return _json_response(_index_resource())


def _index_resource():
    """
    Returns a meme:IndexPage
    """
    return {
            "@type": "meme:IndexPage",
            "recent": _recent_collection(),
        }


def _recent_collection():
    return {
        "@type": "hydra:RecentMemeCollection",
        "member": DB().recent()

    }


if __name__ == '__main__':
    app.run(debug=True)
