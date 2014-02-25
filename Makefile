###===================================================================
### Commands
###===================================================================
all: init deps content

init: init-state

# Install all the deps
deps: .state/py-deps-installed

# Get rid of the generated files
clean: clean-content clean-state

# Generate the example data
content: convert-www-data

# Run this as often as you want the raw data downloaded
data: download-data

###===================================================================
### Subcommands
###===================================================================
init-state:
	@mkdir -p .state

clean-state:
	@rm -rf .state/	

clean-content:
	@rm -rf static/data/

# Get rid of all the downloaded data
clean-data:
	@rm -f data/*

# Download new data
download-data: deps
	@mkdir -p data
	@python bin/memescraper.py

# Converts the example data into the various formats
convert-www-data: static/data static/data/meme.html static/data/meme.n3 static/data/meme.rdf.xml static/data/meme.jsonld


###===================================================================
### Files
###===================================================================
static/data:
	mkdir -p static/data

static/data/meme.jsonld:
	python bin/convert_rdf.py src/meme.html microdata json-ld > static/data/meme.jsonld

static/data/meme.html:
	cp src/meme.html static/data/meme.html

static/data/meme.rdf.xml:
	python bin/convert_rdf.py src/meme.html microdata application/rdf+xml > static/data/meme.rdf.xml

static/data/meme.n3:
	python bin/convert_rdf.py src/meme.html microdata n3 > static/data/meme.n3

# I have to use requirements.txt because there are some 
# repos not on pypi
.state/py-deps-installed: 
	pip install -r requirements.txt
	touch .state/py-deps-installed


