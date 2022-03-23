from frogpy.frog_wrapper import FrogWrapper
import unittest

class FrogWrapperTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.frog = FrogWrapper(config = '/usr/local/etc/frog/frog.cfg', options = { "parser": False })

  def test_analyze(self):
      raw = self.frog.analyse("Dit is een test")
      data = self.frog.parse(raw)
      self.assertEqual(4, len(data))

      self.assertEqual(1, int(data[0]['index']))
      self.assertEqual("Dit", data[0]['text'])
      self.assertEqual("dit", data[0]['lemma'])
      self.assertEqual("[dit]", data[0]['morph'])
      self.assertEqual("VNW(aanw,pron,stan,vol,3o,ev)", data[0]['pos'])
      self.assertLess(0.75, data[0]['posprob'])

  def test_analyse_test_input(self):
    with open('tests/test_input.txt', 'r') as input_file:
      input_text = input_file.read().replace('\n', ' ')
      raw = self.frog.analyse(input_text)

      data = self.frog.parse(raw)
      quote = data[18]

      self.assertEqual('\xe2\x80\x98', quote['text'])
      self.assertEqual("[']", quote['morph'])
      self.assertEqual("'", quote['lemma'])
      self.assertEqual('LET()', quote['pos'])

if __name__ == '__main__':
    unittest.main()
