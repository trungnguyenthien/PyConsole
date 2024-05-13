import json

def json_object(object):
  return json.dumps(vars(dict(object)), indent=2)