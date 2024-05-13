import json

def json_object(object):
  json.dumps(vars(object), indent=2)