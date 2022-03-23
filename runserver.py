#!/usr/bin/env python

from frogpy import app
from os import environ

DEFAULT_HTTP_PORT = 5000

is_development = environ['ENVIRONMENT'] == 'development'
http_port = DEFAULT_HTTP_PORT if 'HTTP_PORT' not in environ else int(environ['HTTP_PORT'])

app.run(debug = is_development, port = http_port)
