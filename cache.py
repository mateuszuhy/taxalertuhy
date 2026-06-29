_cache = None

def get_cache():
    global _cache
    return _cache


def set_cache(data):
    global _cache
    _cache = data
