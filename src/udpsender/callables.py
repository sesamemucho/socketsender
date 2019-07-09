import array
import random


def gen_random(_: object, length: int, **kwds) -> bytes:
    """Generates a bytestring of ramdom values.
    """
    if length is None:
        length = 128

    retval = array.array("B")
    for _ in range(0, length):
        retval.append(random.randrange(0, 256))

    return retval.tobytes()


class UDPS_SequentialSource:
    def __init__(self):
        self.starting_value = 0

    def __call__(self, _: object, length: int, **kwds) -> bytes:
        """Generates a bytestring of sequential values.
        """
        if length is None:
            length = 128

        retval = array.array("B")
        for _ in range(0, length):
            retval.append(self.starting_value)
            self.starting_value = (self.starting_value + 1) % 256

        return retval.tobytes()
