from rdflib import Graph
import sys

in_uri = sys.argv[1]
in_format = sys.argv[2]
out_format = sys.argv[3]

if __name__ == '__main__':
    print Graph().parse(in_uri, format=in_format).serialize(format=out_format),

