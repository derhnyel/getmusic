import os
import vcr
import unittest
from importlib import import_module
from urllib.parse import urlparse
from unittest.mock import patch, MagicMock
from parameterized import parameterized_class

SEARCH_ARGS = ('I love you', 1)
def fetch_engines():
    """ Returns a list of all engines for tests """
    engines = []

    base_dir = os.getcwd()
    engines_dir = os.path.join(base_dir, 'get_music', 'engines')

    for filename in os.listdir(engines_dir):
        if os.path.isfile(os.path.join(engines_dir, filename)) and filename.endswith('.py') \
                and filename != '__init__.py':
            engine = filename.split('.py')[0]
            module = import_module("get_music.engines.{}".format(engine.lower()))
            engine_class = getattr(module, "search")
            engines.append([engine, engine_class(),])
    return engines 

def validate_url(url):
    """ Checks if a url is valid
    urls must contain scheme, netloc and path
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except BaseException:
        print("URL: %s\n" % url)
        return False     

class Test(unittest.TestCase):
    def setUpClass(self):
        from engine.songslover import SongsLover 
        self.engine = SongsLover()
    
    @patch('engine.songslover.Songslover.search')
    @patch('engine.songslover.Songslover.get_response_object')
    async def test_urls_query_and_results(self, get_results_mock, get_soup_mock):
        """ Test that url updates work fine """
        squeryresults = await self.engine.search(query="i love you")
        first_url = self.engine.formated_url.geturl()
        self.assertTrue(validate_url(first_url))
        surlresults = self.engine.search(url="https://songslover.vip/?s=i+love+you")
        second_url = self.engine.formated_url.geturl()

        self.assertTrue(validate_url(second_url))
        self.assertNotEqual(second_url, first_url)

        for key in squeryresults[0]:
            self.assertEqual(squeryresults[0].get(key),surlresults[0].get(key))
        self.assertEqual(squeryresults, surlresults)


    def test_two_queries_different_results(self):
        """ Test that url updates work fine """
        from engine.songslover import SongsLover as slsearch # pylint: disable=import-outside-toplevel
        from engine.justnaija import JustNaija as jnsearch # pylint: disable=import-outside-toplevel
        sengine = slsearch()
        jengine = jnsearch()
        sresults = None
        jresults = None
        with vcr.use_cassette('fixtures/songslover-test-diff-synopsis.yaml', record_mode='once'):
            sresults = sengine.search(query="Donda 2")
        with vcr.use_cassette('fixtures/justnaija-test-diff-synopsis.yaml', record_mode='once'):
            jresults = jengine.search(query="Sungba")
        for key in sresults[0]:
            self.assertNotEqual(sresults[0].get(key),jresults[0].get(key))

        self.assertNotEqual(sresults, jresults)
    

@parameterized_class(('name', 'engine'), fetch_engines())
class TestScraping(unittest.TestCase):
    """ Testbase for Engines

    provides tests for titles, description and return urls
    """
    engine_class = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        try:
            cls.vcr_search(*SEARCH_ARGS)
        except Exception as e:
            print(str(e))
            raise unittest.SkipTest(
                '{} failed due to traffic'.format(
                    cls.engine))

    @classmethod
    def vcr_search(cls, *args, **kwargs):
        print(cls.name)
        with vcr.use_cassette('fixtures/{}-{}-synopsis.yaml'.format(cls.name, args[0].replace(" ", "-")), record="once"):
            cls.results = cls.engine.search(*args, **kwargs)

    
    def test_search_urls(self):
        """
        Test that the search urls generated are valid
        """
        self.assertTrue(validate_url(self.engine.formated_url.geturl()))

    def test_returned_results(self):
        """
        Test that the returned results have valid data. 1 is just a chosen value as most search
        engines return values more than that
        """
        self.assertTrue(len(self.results['title']) >= 1)
        self.assertTrue(len(self.results['category']) >= 1)
        self.assertTrue(len(self.results['artist']) >= 1)
        self.assertTrue(len(self.results['art']) >= 1)
        #self.assertTrue(len(self.results['type']) >= 1)
        #self.assertTrue(len(self.results['download']) >= 1)
        self.assertTrue(len(self.results['details']) >= 1)

    
    #Will be used when search is seperated from parses
    # def test_links(self):
    #     for link in self.results['links']:
    #         print("{}:::::{}".format(self.name, link))
    #         # Sometimes googlescholar returns empty links for citation type results
    #         if not link and self.name.lower() == "googlescholar":
    #             continue
    #         self.assertTrue(validate_url(link))

    def test_results_length_are_the_same(self):
        """ Tests if returned result items are equal.
        :param args: a list/tuple of other keys returned
        """
        # Different engines have different keys which may be returned or not returned
        # So if all keys are not the same length check that the titles and links length are
        # the same
        default_keys = ["title", "category","art","details","artist"]
        for result in self.results:
            default_keys_set = set(map(lambda x: len(result[x]), default_keys))

            items = result.keys()
            items_set = set(map(lambda x: len(result[x]), items))

            self.assertTrue(len(items_set) == 1 or len(default_keys_set) == 1)



   

            