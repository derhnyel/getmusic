import (
    request,
    pdb,
    asyncio,
    aiohttp
)

from urllib.parse import urlparse, urlencode
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup as bs4
from typing import List
import utils.helpers as helpers


class BaseEngine(ABC):
    """
    Base engine from which others engine subclasses
    """

    # Engine properties
    summary: str = None
    name: str = None
    categories: List[str] = []
    site_uri: str = None
    request_methods =
    GET, POST = "get", "post"

    @abstractmethod
    def search(self,query: str=None,page: str=None, 
              category: str=None,**kwargs):
        """ 
        Method to query a particular engine
        """
        raise NotImplementedError()

    
