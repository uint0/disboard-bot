import json
import functools
import collections
import datetime as dt

TTLCacheEntry = collections.namedtuple('TTLCacheEntry', [
    'data',
    'expiry'
])

cached_items = {}

def hash_args(args):
    if isinstance(args, dict):
        return hash_args(tuple(sorted(args.items())))
    
    return tuple(hash(json.dumps(a, sort_keys=True)) for a in args)


def async_cache_ttl(fn=None, /, *, ttl=60, skip_n=0):
    def decorator_builder(fn):
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            top_level_key = hash(fn)
            arg_level_key = (hash_args(args[skip_n:]), hash_args(kwargs))

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