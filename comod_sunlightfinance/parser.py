"""
Must define three methods:

* answer_pattern(pattern, args)
* render_answer_html(answer_data)
* render_answer_json(answer_data)
"""
from .patterns import PATTERNS

import json
from django.template import loader, Context
from random import Random
import requests
import os

def get_api_key():
    key = None
    try:
        key = settings.SUNLIGHT_API_KEY
    except:
        pass
    if 'SUNLIGHT_API_KEY' in os.environ:
        key = os.environ['SUNLIGHT_API_KEY']
    if key == None:
        raise Exception("To use this module, you must have a Sunlight API Key. See the readme here: https://github.com/CivOmega/civomega-mod-sunlightbills/")
    else:
        return key


def legislator_search(**kwargs): #looks up a congressperson given the keywords

    if kwargs != {}:
        url = 'https://congress.api.sunlightfoundation.com/legislators/?apikey=%s' % (get_api_key())
        params  = ''.join('&%s=%s' % pair for pair in kwargs.iteritems())
        resp = requests.get(url+params)
        return resp.json()
    else:
        return {}

def fec_query_by_legislator(names):
    for name in names:


        
        legislator = legislator_search(name=name)
        legislator_fec_ids = legislator['results'][0]['fec_ids']








############################################################
# Pattern-dependent behavior
def answer_pattern(pattern, args):
    """
    Returns a `dict` representing the answer to the given
    pattern & pattern args.

    'plaintxt' should always be a returned field

    """
    if pattern not in PATTERNS:
      return None
    if len(args) != 1:
      return None

    return {
      'plaintxt': ''
    }

############################################################
# Applicable module-wide
def render_answer_html(answer_data):
    template = loader.get_template('comod_example/example.html')
    return template.render(Context(answer_data))

def render_answer_json(answer_data):
    return json.dumps(answer_data)
