from flask import request
import frogpy
from frogpy import app, logger, resources
from frogpy.frog_wrapper import FrogWrapper
import unittest
from tests.cache_test import get_test_cache
import werkzeug.exceptions

VALID_REQUEST = {
  'content_type': 'text/plain',
  'data': 'Dit is een test',
  'headers': {'Authorization': 'goodToken'}
}

class AnalyseTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    frog = FrogWrapper(config='/usr/local/etc/frog/frog.cfg', options={ "parser": False })
    resources.get_frog = lambda: frog

  def setUp(self):
    app.config['AUTH_TOKEN'] = 'goodToken'
    test_cache = get_test_cache()
    resources.get_cache = lambda: test_cache
    self.endpoint = resources.Analyse()

  def test__checkAuthorization(self):
    # With no Authorization header in the request
    with app.test_request_context():
      with self.assertRaises(werkzeug.exceptions.Unauthorized):
        self.endpoint._checkAuthorization()

    # Authorization header given, but the system doesn't have the AUTH_TOKEN config parameter
    del app.config['AUTH_TOKEN']
    with app.test_request_context(headers={'Authorization': 'test'}):
      with self.assertRaises(werkzeug.exceptions.InternalServerError):
        self.endpoint._checkAuthorization()

    # Invalid Authorization header given
    app.config['AUTH_TOKEN'] = 'test'
    with app.test_request_context(headers={'Authorization': 'badToken'}):
      with self.assertRaises(werkzeug.exceptions.Unauthorized):
        self.endpoint._checkAuthorization()

    # Valid Authorization header given
    app.config['AUTH_TOKEN'] = 'test'
    with app.test_request_context(headers={'Authorization': 'test'}):
      self.endpoint._checkAuthorization()

  def test__checkContentType(self):
    # With empty content type
    with app.test_request_context():
      with self.assertRaises(werkzeug.exceptions.UnsupportedMediaType):
        logger.info(request.environ['CONTENT_TYPE'])
        self.endpoint._checkContentType()

    # With valid content type
    with app.test_request_context(content_type='text/plain'):
      self.endpoint._checkContentType()

  def test_delete(self):
    with app.test_request_context(**VALID_REQUEST):
      with self.assertRaises(werkzeug.exceptions.NotFound):
        self.endpoint.delete()

  def test_get(self):
    with app.test_request_context(**VALID_REQUEST):
      with self.assertRaises(werkzeug.exceptions.NotFound):
        self.endpoint.get()

  def test_post(self):
    with app.test_request_context(**VALID_REQUEST):
      self.endpoint.post()

if __name__ == '__main__':
  unittest.main()
