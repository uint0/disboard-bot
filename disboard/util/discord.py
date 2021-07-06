import functools


def cache_command():
    pass


def require_channel(channel):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, ctx, *args, **kwargs):
            if str(ctx.channel.id) != str(channel):
                return None
            return await func(self, ctx, *args, **kwargs)
        return wrapper
    return decorator


def raises_exception(exc_type):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, ctx, *args, **kwargs):
            try:
                return await func(self, ctx, *args, **kwargs)
            except exc_type as ex:
                return await ctx.send(ex.args[0])
        return wrapper
    return decorator