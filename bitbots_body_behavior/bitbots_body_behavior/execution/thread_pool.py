from concurrent.futures import ThreadPoolExecutor as TPExecutor


class ThreadPoolExecutor:
    def __init__(self, max_workers=10):
        self.executor = TPExecutor(max_workers=max_workers)

    def map(self, func, iterables):
        return self.executor.map(func, iterables)

    def submit(self, func, *args, **kwargs):
        return self.executor.submit(func, *args, **kwargs)
