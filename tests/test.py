import unittest
from urllib.request import urlopen
from bs4 import BeautifulSoup



class Test(unittest.TestCase):
    
    parent_object = None
    single_object= None
    query = {}
    
    def setUpClass():
        url = "engine_url" 
        Test.soup = BeautifulSoup(urlopen(url),'html.parser')
    
    def test_parse_parent_object(self):
      self.assertEqual('Python', pageTitle);
    
    def test_parse_single_object(self):
      self.assertIsNotNone(content)
    
    def test_search(self):
       self.assertIsInstance(engine.search(self.soup), str)

if __name__ == '__main__':
   unittest.main()    

   

            