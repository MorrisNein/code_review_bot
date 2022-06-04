import asyncio
import datetime

lock = asyncio.Lock()


def async_lock(function):
    """Acquires the lock on a function that should be executed by
    only one thread at a time"""
    async def wrapper(*args, **kwargs):
        async with lock:
            print(f'Lock acquired: {datetime.datetime.now()}')
            result = await function(*args, **kwargs)
        print(f'Lock released: {datetime.datetime.now()}')
        return result
    return wrapper
