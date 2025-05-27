import functools


def catch_exception(logger, placeholder: str = None):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"{placeholder or 'Ошибка'}:\n{e}")
                raise
        return wrapper
    return decorator


def silent_exception():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception:
                pass
        return wrapper
    return decorator
