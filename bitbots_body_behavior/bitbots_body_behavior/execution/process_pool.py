from concurrent.futures import ProcessPoolExecutor as PPExecutor


class ProcessPoolExecutor:
    def __init__(self, max_workers=10):
        self.executor = PPExecutor(max_workers=max_workers)

    def map(self, func, iterables, chunksize=1):
        return self.executor.map(func, iterables, chunksize=chunksize)

    def submit(self, func, *args, **kwargs):
        return self.executor.submit(func, *args, **kwargs)
