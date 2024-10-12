from abc import abstractmethod
import os
import json
from helper_functions import get_files_by_access_time

class Cache:
    @abstractmethod
    def __getitem__(self, item):
        pass

    @abstractmethod
    def __setitem__(self, key, value):
        pass


class INFCache(Cache):
    def __init__(self):
        self._cache = {}

    def __len__(self):
        return len(self._cache.keys())

    def __getitem__(self, key):
        if key in self._cache.keys():
            return self._cache[key]
        else:
            return KeyError(f"Key [{key}] was not found in {self}")

    def __setitem__(self, key, value):
        """ Operator for setting the value at a specified key in the INF_Cache """
        # add new value to cache
        self._cache[key] = value
        return self._cache[key]

    @property
    def keys(self):
        return self._cache.keys()


class LRUCache(Cache):
    """ Cache Object that stores data as a dictionary with a max number of entries """
    def __init__(self, max_entries: int = 64):
        self._cache = {}
        self._key_list = []
        self._max_entries = max_entries

    def __len__(self):
        return len(self._cache.keys())

    def __getitem__(self, key):
        if key in self._key_list:
            self._key_list.remove(key)
            self._key_list.insert(0, key)
            return self._cache[key]
        else:
            return KeyError(f"Key [{key}] was not found in {self}")

    def __setitem__(self, key, value):
        """Operator for setting the value at a specified key in the LRU_Cache"""
        # if the key is already in the key_list, set a new value and move it to the top of the key_list
        if key in self._key_list:
            self._cache[key] = value
            self._key_list.remove(key)
            self._key_list.insert(0, key)
            return self._cache[key]

        # if cache is full, discard latest entry
        if len(self) >= self._max_entries:
            latest_key = self._key_list[-1]
            del self._cache[latest_key]
            self._key_list.remove(latest_key)

        # add the new value to the head of the list
        self._key_list.insert(0, key)

        # add new value to cache
        self._cache[key] = value

        return self._cache[key]

    @property
    def keys(self):
        return self._key_list


class EXTERNALCache(Cache):
    """ Used to store data between process executions for things like API calls """
    def __init__(self, max_size: int = 64, dir_path: str = "./ExternalCache/"):
        self._max_size = max_size
        if dir_path[-1] != '/':
            dir_path += '/'
        self._dir_path = dir_path
        if not os.path.exists(self._dir_path):
            os.makedirs(self._dir_path)
        self._keys = get_files_by_access_time(self._dir_path, remove_extension=True)


    def __len__(self):
        return len(self._keys)

    def __getitem__(self, key):
        if key + '.json' in os.listdir(self._dir_path):
            with open(self._dir_path + key + '.json', "r") as file:
                data = json.load(file)
            self._keys.remove(key)
            self._keys.insert(0, key)
            return data
        else:
            return KeyError(f"Key [{key}] not found in ({self})")

    def __setitem__(self, key: str, value: dict):
        # check if key already exists
        if key + '.json' in os.listdir(self._dir_path):
            with open(self._dir_path + key + '.json', "w") as file:
                json.dump(value, file)
            self._keys.remove(key)
            self._keys.insert(0, key)
            return self._dir_path + key
        # check if cache exceeds maximum size
        if len(self) >= self._max_size:
            os.remove(self._dir_path + self._keys[-1] + '.json')
        # add file to the cache
        with open(self._dir_path + key + '.json', "w") as file:
            json.dump(value, file)
        self._keys.insert(0, key)
        return self._dir_path + key

    @property
    def keys(self):
        return self._keys

    @property
    def max_size(self):
        return self._max_size

    @property
    def dir_path(self):
        return self._dir_path
