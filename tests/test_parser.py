import unittest

from scraper import MyHTMLParser

class TestParser(unittest.TestCase):
  def setUp(self):
    self.parser = MyHTMLParser()

  def test_finds_css_links(self):
      self.parser.feed('<link rel="stylesheet" href="/style.css" />')
      self.assertEqual(self.parser.css, ['/style.css'])

  def test_finds_js_script_links(self):
    self.parser.feed('<script src="/launch.js" />')
    self.assertEqual(self.parser.scripts, ['/launch.js'])

  def test_finds_url_links(self):
    self.parser.feed('<a href="http://www.google.com/" />')
    self.assertEqual(self.parser.links, ['http://www.google.com/'])

  def test_finds_embedded_images(self):
    self.parser.feed('<img src="/icon.jpeg" />')
    self.assertEqual(self.parser.images, ['/icon.jpeg'])
