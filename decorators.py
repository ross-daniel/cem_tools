import time
import caches


def get_time(func):
    """ Decorator to record execution time of a function """

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"execution took {end - start} seconds")
        return result

    return wrapper


def memoize(func):
    """ Decorator to cache function calls"""
    cache = caches.EXTERNALCache()

    def wrapper(*args, **kwargs):
        if f"{str(func.__name__)}{str(args)}{str(kwargs)}" in cache.keys:
            return cache[f"{str(func.__name__)}{str(args)}{str(kwargs)}"]
        else:
            cache[f"{str(func.__name__)}{str(args)}{str(kwargs)}"] = func(*args, **kwargs)
            return cache[f"{str(func.__name__)}{str(args)}{str(kwargs)}"]

    return wrapper
