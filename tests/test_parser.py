import unittest

from pyquery import PyQuery as pq

from SiteCrawler.Parser import MasterPageParser, ProductPageParser


class TestMasterPageParser(unittest.TestCase):
  def setUp(self):
    self.parser = MasterPageParser('hello')

  def test_find_product_page_links(self):
      self.parser.py_query = pq('<ul class="productLister"><li><h3 class="productInfo"><a href="blah"></h3></li></ul>')
      results = self.parser.GetResults()
      
      self.assertEqual(results, ['blah'])


class TestProductPageParser(unittest.TestCase):
  def setUp(self):
    self.parser = ProductPageParser('hello')
  
  def test_description(self):
    self.parser.py_query = pq('<div><h3 class="productDataItemHeader">Description</h3><div><p>Apricots</p></div></div>')
    results = self.parser.GetResults()
    
    self.assertEqual(results['description'], 'Apricots')

  def test_finds_unit_price(self):
    self.parser.py_query = pq('<div class="pricing"><div class="pricePerUnit">$3.45</div></div>')
    results = self.parser.GetResults()
    
    self.assertEqual(results['unit_price'], 3.45)
