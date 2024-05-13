import json

def json_object(object):
  return json.dumps(vars(object), indent=2)