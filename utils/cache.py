import pickle
import hashlib
import os

class Cache:
    def __init__(self,path): 

        caller_path = path
        self.cache = os.path.join(caller_path,"__cache__")
        if not os.path.exists(self.cache):
            os.makedirs(self.cache)
        caller_dir_list = os.listdir(caller_path)
        self.caller_cache = {file[:-3]: os.path.join(self.cache, file[:-3]) for file in caller_dir_list if file not in ("__init__.py","cache","__main__.py")}
        for cache in self.caller_cache.values():
            if not os.path.exists(cache):
                os.makedirs(cache)
    
    #Do not cache the search / fetch result . Instead Cache the Individual songs url results
    def put_update(self,caller,url,items,cache=True):
        cache_path,_= self._cache_hit(caller,url)
        with open(cache_path, 'wb') as stream:
            pickle.dump(items, stream)
            return items,True

    def retrieve(self, caller,url,temp_dir=None, cache=True):
        cache_path,cache_hit = self._cache_hit(caller, url)
        if cache_hit and cache:
            with open(cache_path, 'rb') as stream:
                cache_object = (pickle.load(stream), True)
            # check if cached object is still in temp directory
            if temp_dir is None or (temp_dir is not None and os.path.exists(cache_object[0])):
                return cache_object                
        return None,False        

    def _cache_hit(self,caller,url):
        urlhash = hashlib.sha256(url.encode("utf-8")).hexdigest()
        caller = caller.lower()
        cache_path = os.path.join(self.caller_cache[caller], urlhash)
        return cache_path,os.path.exists(cache_path)

    def clear(self, caller=None):
        """
        Clear the entire cache either by caller name
        or all
        :param caller: caller to clear
        """
        if not caller:
            for caller_cache in self.caller_cache.values():
                for root, dirs, files in os.walk(caller_cache):
                    for file in files:
                        os.remove(os.path.join(caller_cache, file))
        else:
            caller_cache = self.caller_cache[caller.lower()]
            for _, _, files in os.walk(caller_cache):
                for file in files:
                    os.remove(os.path.join(caller_cache, file))
