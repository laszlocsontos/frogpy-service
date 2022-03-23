from frog import Frog, FrogOptions
from frogpy import app, logger
from time import time

class FrogWrapper:

  def __init__(self, config=None, options=None):
    try:
      self.config = app.config['FROG_CONFIG']
    except KeyError, ke:
      logger.debug(ke)

    if config is not None:
      self.config = config

    self.options = None
    try:
      self.options = app.config['FROG_OPTIONS']
    except KeyError, ke:
      logger.debug(ke)

    if options is not None:
      self.options = options

    logger.info("Initializing Frog with options=\"%s\", config=\"%s\"", self.options, self.config)
    self.frog = Frog(FrogOptions(**self.options), self.config)

  def analyse(self, input):
    startTime = time()

    logger.debug("Processing input \"%s\"", input)
    raw = self.frog.process_raw(input)

    endTime = time()
    logger.debug("Processing finished, under %f ms", round((endTime - startTime) * 1000))

    # Workaround for "TypeError: Argument 'response' has incorrect type (expected str, got unicode)"
    if type(raw) == unicode:
      raw = raw.encode('utf-8')

    return raw

  def parse(self, raw):
    return self.frog.parsecolumns(raw)
