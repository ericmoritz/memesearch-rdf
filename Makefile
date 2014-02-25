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
	@rm -rf priv/www/data/

# Get rid of all the downloaded data
clean-data:
	@rm -f data/*

# Download new data
download-data: deps
	@mkdir -p data
	@python bin/memescraper.py

# Converts the example data into the various formats
convert-www-data: priv/www/data priv/www/data/meme.html priv/www/data/meme.n3 priv/www/data/meme.rdf.xml priv/www/data/meme.jsonld


###===================================================================
### Files
###===================================================================
priv/www/data:
	mkdir -p priv/www/data

priv/www/data/meme.jsonld:
	python bin/convert_rdf.py priv/www/src/meme.html microdata json-ld > priv/www/data/meme.jsonld

priv/www/data/meme.html:
	cp priv/www/src/meme.html priv/www/data/meme.html

priv/www/data/meme.rdf.xml:
	python bin/convert_rdf.py priv/www/src/meme.html microdata application/rdf+xml > priv/www/data/meme.rdf.xml

priv/www/data/meme.n3:
	python bin/convert_rdf.py priv/www/src/meme.html microdata n3 > priv/www/data/meme.n3

# I have to use requirements.txt because there are some 
# repos not on pypi
.state/py-deps-installed: 
	pip install -r requirements.txt
	touch .state/py-deps-installed


