import array
import random

SEQUENTIAL_VALUE = 0


def gen_random(length: int) -> bytes:
    if length is None:
        length = 128

    retval = array.array("B")
    for i in range(0, length):
        retval.append(random.randrange(0, 256))

    return retval.tobytes()


def gen_sequential(length: int) -> bytes:
    global SEQUENTIAL_VALUE
    if length is None:
        length = 128

    retval = array.array("B")
    for i in range(0, length):
        retval.append(SEQUENTIAL_VALUE)
        SEQUENTIAL_VALUE = (SEQUENTIAL_VALUE + 1) % 256

    return retval.tobytes()
