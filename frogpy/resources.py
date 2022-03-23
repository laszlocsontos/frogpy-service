from cache import CacheKey
from flask import abort, make_response, request
from flask.ext import restful
from frogpy import api, app, cacheInstance, frogInstance, logger
import httplib

def get_cache():
  return cacheInstance

def get_frog():
  return frogInstance

class Analyse(restful.Resource):

  def delete(self):
    data = self._processRequest()
    cacheKey = self._buildCacheKey(data)

    result = get_cache().delete(cacheKey)
    if result < 1:
      abort(httplib.NOT_FOUND)

    return make_response("", httplib.NO_CONTENT)

  def get(self):
    data = self._processRequest()
    cacheKey = self._buildCacheKey(data)

    value = get_cache().get(cacheKey)
    if value is None:
      abort(httplib.NOT_FOUND)

    logger.debug("GET value=%s", value)

    return self._transformResponse(value)

  def post(self):
    data = self._processRequest()
    cacheKey = self._buildCacheKey(data)

    value = get_cache().get(cacheKey, updateTTL = True)
    if value is not None:
      return self._transformResponse(value)

    value = get_frog().analyse(data)
    oldValue = get_cache().getAndSet(cacheKey, value)

    logger.debug("POST value=%s, oldValue=%s", value, oldValue)

    if oldValue is not None:
      return self._transformResponse(oldValue)

    return self._transformResponse(value)

  def _buildCacheKey(self, data):
    cacheKey = CacheKey(namespace='frog', data=data, options=get_frog().options)
    logger.debug('Cache key for data="%s", options="%s" is "%s"', data, get_frog().options, cacheKey.build())
    return cacheKey

  def _checkAuthorization(self):
    if 'Authorization' not in request.headers:
      abort(httplib.UNAUTHORIZED)

    authorization = request.headers.get('Authorization')

    try:
      if authorization != app.config['AUTH_TOKEN']:
        logger.debug("Unauthorized token %s", authorization)
        abort(httplib.UNAUTHORIZED)
    except KeyError:
      logger.error("Environment variable AUTH_TOKEN has not been set")
      abort(httplib.INTERNAL_SERVER_ERROR)

  def _checkContentType(self):
    contentType = request.environ['CONTENT_TYPE']
    if contentType != 'text/plain':
      logger.debug("Unsupported media type %s", contentType)
      abort(httplib.UNSUPPORTED_MEDIA_TYPE)

  def _processRequest(self):
    self._checkAuthorization()
    self._checkContentType()
    return request.data

  def _transformResponse(self, data):
    if 'Accept' not in request.headers:
      return data
    if request.headers.get('Accept') != 'application/json':
      return data
    return get_frog().parse(data)

class Root(restful.Resource):
  def get(self):
    return { 'status': 'OK' }

api.add_resource(Analyse, '/analyse')
api.add_resource(Root, '/')
