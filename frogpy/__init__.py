from flask import Flask, Response
from flask.ext import restful
from flask import make_response
from json import dumps, loads
import logging
from os import environ
import sys

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.DEBUG)

logger = logging.getLogger(__name__)

DEFAULT_FROG_CONTIG = '/usr/local/etc/frog/frog.cfg'
DEFAULT_FROG_OPTIONS = '{ "parser": "False" }'
DEFAULT_REDIS_HOST = 'localhost'
DEFAULT_REDIS_PORT = 6379
DEFAULT_REDIS_DB = 0

app = Flask(__name__)

def configure(key, defaultValue):
  value = environ.get(key)
  if not value:
    value = defaultValue
  else:
    logger.debug('Detected environment variable %s = %s', key, value)

  try:
    app.config[key] = loads(value)
  except:
    error = sys.exc_info()[1]
    logger.debug('Key \"%s\" could not be deserialized from JSON, using string \"%s\" instead; reason: %s', key, value, error)
    app.config[key] = value

  logger.info('Using environment variable %s = %s', key, app.config[key])

def output_json(obj, code, headers=None):
  data = dumps(obj, default=(lambda o: o.__dict__))
  resp = make_response(data, code)

  headers = headers or {}
  headers['Content-Type'] = 'application/json'
  headers['Content-Length'] = len(data)

  resp.headers.extend(headers)
  return resp

def output_text(obj, code, headers=None):
  data = str(obj)
  resp = make_response(data, code)

  headers = headers or {}
  headers['Content-Type'] = 'application/json'
  headers['Content-Length'] = len(data)

  resp.headers.extend(headers)
  return resp

DEFAULT_REPRESENTATIONS = {
  'text/plain': output_text,
  'application/json': output_json
}

api = restful.Api(app)
api.representations = DEFAULT_REPRESENTATIONS

cacheInstance = None
frogInstance = None

if 'ENVIRONMENT' in environ:
  configure('AUTH_TOKEN', "")

  from cache import Cache

  configure('REDIS_HOST', DEFAULT_REDIS_HOST)
  configure('REDIS_PORT', DEFAULT_REDIS_PORT)
  configure('REDIS_DB', DEFAULT_REDIS_DB)

  global cacheInstance
  cacheInstance = Cache()

  from frog_wrapper import FrogWrapper

  configure('FROG_CONFIG', DEFAULT_FROG_CONTIG)
  configure('FROG_OPTIONS', DEFAULT_FROG_OPTIONS)

  global frogInstance
  frogInstance = FrogWrapper()

import frogpy.resources
import frogpy.frog_wrapper

logger.info('Module %s initialized' % __name__)
