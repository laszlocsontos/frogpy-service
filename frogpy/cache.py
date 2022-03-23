from datetime import datetime, timedelta
from hashlib import sha256
from frogpy import app, logger
from Queue import Queue
from redis import StrictRedis
import sys
from threading import Thread

class Cache:

  def __init__(self, host = None, port = None, db = None, redis = None):
    try:
      self.host = app.config['REDIS_HOST']
    except KeyError:
      pass

    if host is not None:
      self.host = host

    try:
      self.port = app.config['REDIS_PORT']
    except KeyError:
      pass

    if port is not None:
      self.port = port

    try:
      self.db = app.config['REDIS_DB']
    except KeyError:
      pass

    self.db = 0
    if db is not None:
      self.db = db

    if redis is not None:
      self.redis = redis
    else:
      port = int(self.port)
      db = int(self.db)
      logger.info('Connecting to Redis; host = "%s", port = %s, db = %s', self.host, port, db)
      self.redis = StrictRedis(host = self.host, port = port, db = db)

    self.expirationQueue = Queue()

    expirationUpdater = CacheExpirationUpdater(self.expirationQueue, self)
    expirationUpdater.start()

  def delete(self, cacheKey):
    key = cacheKey.build()
    return self.redis.delete(key)

  def get(self, cacheKey, updateTTL = False):
    key = cacheKey.build()
    value = self.redis.get(key)
    if value is not None and updateTTL:
      self.expirationQueue.put(key)
    return value

  def getTTL(self, cacheKey):
    key = cacheKey.build()
    return self.redis.ttl(key)

  def getAndSet(self, cacheKey, value):
    key = cacheKey.build()
    value = self.redis.getset(key, value)
    self.expirationQueue.put(key)
    return value

  def set(self, cacheKey, value):
    key = cacheKey.build()
    self.redis.set(key, value)
    self.expirationQueue.put(key)

  def setExpire(self, key):
    if not self.redis.exists(key):
      logger.debug('Cound not set expiration for non-existent key %s', key)
      return

    now = datetime.utcnow()
    delta = timedelta(days = 1)
    when = now + delta

    logger.debug('Setting expiration %s for key %s', when, key)
    self.redis.expireat(key, when)

class CacheExpirationUpdater(Thread):

  def __init__(self, queue, cache):
    Thread.__init__(self)
    self.daemon = True
    self.queue = queue
    self.cache = cache

  def run(self):
    while True:
      key = self.queue.get()
      try:
        self.cache.setExpire(key)
      except:
        logger.error('Unexpected error: %s', sys.exc_info()[0])
      self.queue.task_done()

class CacheKey:

  def __init__(self, namespace, **kwargs):
    self.namespace = namespace
    self.fields = kwargs
    self.key = None

  def __setattr__(self, name, value):
    if name != 'key':
      self.__dict__[name] = value
      self.__dict__['key'] = None
    else:
      self.__dict__['key'] = value

  def __str__(self):
    return self.build()

  def build(self):
    if self.key is None:
      name = str(self.fields)
      if len(name) > 32:
        name = sha256(name).hexdigest()
      self.key = ':'.join([self.namespace, name])
    return self.key
