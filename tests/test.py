import unittest
import json as js
from urllib.request import urlopen
from bs4 import BeautifulSoup
from engine.songslover import Songslover as Engine


class Test(unittest.TestCase,Engine):
    
    def setUpClass(url,json=False):
        content = urlopen(url)
        return js.loads(content) if json else BeautifulSoup(content,'html.parser')
    
    def test_parse_parent_object(self):
        url="<parent url>"
        parent_object = self.setUpclass(url)
        response = self.parse_parent_object(parent_object)
        #item url should be equal to a particular value
        self.assertEqual('<get link to an item>', response)
    
    def test_parse_single_object(self):
       url="<single url>"
       single_object = self.setUpclass(url)
       response = self.parse_single_object(single_object)
       self.assertIsNotNone(response)#download link value shouldn't be None
    
    def test_search(self):
       response= self.search(query={})
       #search should return a value and should be a dict object 
       self.assertIsInstance(response,dict)

if __name__ == '__main__':
   unittest.main()    

   

            