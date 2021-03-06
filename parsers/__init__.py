#!/usr/bin/python

# To start tracking a new site:
#  - create a parser class in another file, based off (say) bbc.BBCParser
#  - add it to parsers (below)
# Test with test_parser.py

# List of parsers to import and use based on parser.domains

parsers = """
nyt.NYTParser
cnn.CNNParser
politico.PoliticoParser
bbc.BBCParser
""".split()

# washpo.WashPoParser

parser_dict = {}

# Import the parsers and fill in parser_dict: domain -> parser
for parser_name in parsers:
    module, classname = parser_name.rsplit('.', 1)
    parser = getattr(__import__(module, globals(), fromlist=[classname]), classname)
    for domain in parser.domains:
        parser_dict[domain] = parser


def get_parser(url):
    return parser_dict[url.split('/')[2]]


# Each feeder places URLs into the database to be checked periodically.

parsers = [parser for parser in parser_dict.values()]

__all__ = ['parsers', 'get_parser']
