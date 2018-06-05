#!/usr/bin/env python

import yaml

def get_params(filename):
    with open(filename, 'r') as stream:
        try:
            params = yaml.load(stream)
        except yaml.YAMLError as exc:
            raise Exception('Bad YAML File Read')
            print(exc)
    params = dict([a, str(x)] for a, x in params.items())
    return params



