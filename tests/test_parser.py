import unittest

# from scraper import MyHTMLParser
from SiteCrawler.Parser import MasterPageParser, ProductPageParser


class TestParser(unittest.TestCase):
  def setUp(self):
    self.parser = MasterPageParser()
    self.parser.py_query = pq('')

  def test_finds_css_links(self):
      '<ul class="productLister"><li><h3></h3></li></ul>'
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
