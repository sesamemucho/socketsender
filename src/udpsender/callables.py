import array
import random


class UDPS_GenRandom:
    def __init__(self, sched: object) -> None:
        self.sched = sched
        if sched.length is None:
            self.length = 128
        else:
            self.length = sched.length

    def __call__(self, **kwds) -> bytes:
        """Generates a bytestring of ramdom values.
        """
        retval = array.array("B")
        for _ in range(0, self.length):
            retval.append(random.randrange(0, 256))

        return retval.tobytes()


class UDPS_SequentialSource:
    def __init__(self, sched: object) -> None:
        self.sched = sched
        self.starting_value = 0
        if sched.length is None:
            self.length = 128
        else:
            self.length = sched.length

    def __call__(self, **kwds) -> bytes:
        """Generates a bytestring of sequential values.
        """
        retval = array.array("B")
        for _ in range(0, self.length):
            retval.append(self.starting_value)
            self.starting_value = (self.starting_value + 1) % 256

        return retval.tobytes()


class UDPS_FileSource:
    def __init__(self, sched: object) -> None:
        self.sched = sched
        if sched.length is None:
            self.length = 128
        else:
            self.length = sched.length

        self.fd = open(sched.user_data["user_data1"], "r")

    def __call__(self, **kwds) -> bytes:
        """Generates a bytestring of sequential values.
        """
        data = self.fd.read(self.length)
        return data.encode()
