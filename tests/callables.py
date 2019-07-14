"""This file contains function definitions used by tests.
"""

import time

class UDPS_Test1:
    def __init__(self, _: object) -> None:
        pass

    def __call__(self, **kwds) -> bytes:
        return b"Hello"

class UDPS_Test2:
    def __init__(self, _: object) -> None:
        pass

    def __call__(self, **kwds) -> bytes:
        time.sleep(0.5)
        return b"Hello"
