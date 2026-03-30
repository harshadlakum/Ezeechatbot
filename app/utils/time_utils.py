import time


class Timer:
    def __init__(self):
        self._start = None

    def start(self):
        self._start = time.perf_counter()

    def elapsed_ms(self) -> float:
        if self._start is None:
            return 0.0
        return round((time.perf_counter() - self._start) * 1000, 2)
