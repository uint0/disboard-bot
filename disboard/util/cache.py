import functools
import collections
import datetime as dt

TTLCacheEntry = collections.namedtuple('TTLCacheEntry', [
    'data',
    'expiry'
])

cached_items = {}

def async_cache_ttl(fn=None, /, *, ttl=60):
    def decorator_builder(fn):
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            top_level_key = hash(fn)
            arg_level_key = ((args), tuple(sorted(kwargs.items())))

            cached = cached_items.get(top_level_key, {}).get(arg_level_key)
            
            if cached is None or dt.datetime.now() > cached.expiry:
                cached = TTLCacheEntry(
                    data=await fn(*args, **kwargs),
                    expiry=dt.datetime.now() + dt.timedelta(seconds=ttl)
                )

                cached_items.setdefault(top_level_key, {})[arg_level_key] = cached

            return cached.data

        return wrapper

    return decorator_builder(fn) if fn else decorator_builder