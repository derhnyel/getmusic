import inspect
import pickle
import hashlib


#FILEPATH = os.path.dirname(os.path.abspath(__file__))


def __get_caller_stack(active=False):
        # Get the full stack
        frame_stack = inspect.stack()
        # Get one level up from current
        if active:
            caller_frame_record = frame_stack[-4]
        else:
            caller_frame_record = frame_stack[-1]
        return caller_frame_record
        #caller_file_name = CallerFrame.filename  # Filename where caller lives

def __get_caller_path():
    # Get the module object of the caller
    calling_script = inspect.getmodule(__get_caller_stack()[0])
    if calling_script == None:
       calling_script = inspect.getmodule(__get_caller_stack(active=True)[0])
       #module name from this path
    caller_path = os.path.dirname(calling_script.__file__)
    return caller_path

class Cache:
    def __init__(self): 
        caller_path = __get_caller_path()
        self.cache = os.path.join(caller_path,"cache")
        if not os.path.exists(self.cache):
            os.makedirs(self.cache)
        caller_dir_list = os.listdir(caller_path)
        self.caller_cache = {file[:-3]: os.path.join(self.cache, file[:-3]) for file in caller_dir_list if file not in ("__init__.py","cache","__main__.py")}
        for cache in self.caller_cache.values():
            if not os.path.exists(cache):
                os.makedirs(cache)

    def put_update_retrieve(self,caller,url,results=None,cache=True):
        urlhash = hashlib.sha256(url.encode("utf-8")).hexdigest()
        caller = caller.lower()
        cache_path = os.path.join(self.caller_cache[caller], urlhash)
        # Retrieve Item from Cache
        if os.path.exists(cache_path) and cache:
            with open(cache_path, 'rb') as stream:
                return pickle.load(stream), True
        # Put_Update item in Cache       
        with open(cache_path, 'wb') as stream:
            pickle.dump(results, stream)
            return results, False

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
                for f in files:
                    os.remove(os.path.join(caller_cache, f))
