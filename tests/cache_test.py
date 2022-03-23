from frogpy.cache import Cache, CacheKey
from frogpy import logger
from os import environ
from time import sleep
import unittest
import uuid

def get_test_cache():
  if 'REDIS_HOST' not in environ or 'REDIS_PORT' not in environ:
    logger.info('Using dummy Redis store instead a real one')
    dummyRedis = DummyRedis()
    return Cache(redis=dummyRedis)
  else:
    redisHost = environ['REDIS_HOST']
    redisPort = environ['REDIS_PORT']
    return Cache(host=redisHost, port=redisPort)

class CacheTest(unittest.TestCase):

  def setUp(self):
    self.cache = get_test_cache()

  def test_delete(self):
    cacheKey = CacheKey(namespace='frog', data='key1')
    self.cache.set(cacheKey, 'value')
    self.cache.delete(cacheKey)
    value = self.cache.get(cacheKey)
    self.assertIsNone(value)

  def test_get(self):
    value = self.cache.get(CacheKey(namespace='frog', data=str(uuid.uuid4())))
    self.assertIsNone(value)

  def test_getAndSet(self):
    cacheKey = CacheKey(namespace='frog', data=str(uuid.uuid4()))
    value = self.cache.getAndSet(cacheKey, 'value')
    self.assertIsNone(value)
    value = self.cache.get(cacheKey)
    self.assertEqual('value', value)

  def test_set(self):
    cacheKey = CacheKey(namespace='frog', data='key1')
    self.cache.set(cacheKey, 'value')
    value = self.cache.get(cacheKey)
    self.assertEqual('value', value)

    sleep(5)

class CacheKeyTest(unittest.TestCase):

  def test_build(self):
    cacheKey = CacheKey(namespace='frog', data='Dit is een test')
    key = cacheKey.build()
    self.assertEqual("frog:{'data': 'Dit is een test'}", key)

    cacheKey = CacheKey(namespace='frog', data='01234567890123456789012345678901')
    key = cacheKey.build()
    self.assertEqual('frog:4ec2b5c65994c157660dd662e0e37d4fd7eb77fe3d93c3d814550ae3142142df', key)

class DummyRedis():

  def __init__(self):
    self.cache_entries = {}
    self.cache_ttls = {}

  def delete(self, key):
    try:
      del self.cache_entries[key]
      del self.cache_ttls[key]
    except KeyError, ke:
      logger.debug(ke)

  def exists(self, key):
    return key in self.cache_entries

  def get(self, key):
    try:
      return self.cache_entries[key]
    except KeyError:
      return None

  def getset(self, key, value):
    oldValue = self.get(key)
    self.cache_entries[key] = value
    return oldValue

  def set(self, key, value):
    self.cache_entries[key] = value

  def expireat(self, key, when):
    self.cache_ttls[key] = when
    logger.debug('Setting expiration %s for key %s', when, key)

  def ttl(self, key):
    try:
      return self.cache_ttls[key]
    except KeyError:
      return -1

if __name__ == '__main__':
    unittest.main()
