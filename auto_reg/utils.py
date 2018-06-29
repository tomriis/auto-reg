#!/usr/bin/env python

import ruamel.yaml

def get_params(filename):
    with open(filename, 'r') as _f:
        return ruamel.yaml.round_trip_load(_f.read(), preserve_quotes=True)
    
def set_params(filename, params):
    with open(filename, 'w') as _f:
        _f.write(ruamel.yaml.dump(params, Dumper=ruamel.yaml.RoundTripDumper, width=1024))

