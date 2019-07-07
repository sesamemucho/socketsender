"""Sends UDP packets on a schedule.
"""

import array
import collections.abc


class NextBuffer:
    def __init__(self):
        self.value = 0

    def get(self, blocksize):
        # For now, make sure blocksize is even
        if blocksize % 2 != 0:
            raise ValueError()
        a = array.array("H", range(self.value, self.value + blocksize))
        self.value += blocksize
        return a.tobytes()


class DefaultWrapper:
    def __init__(self, src_socket=None):
        self.next_buffer = NextBuffer()
        # self.src_socket = src_socket()

    def send(self, cfg):
        data = self.next_buffer.get(cfg.size)


class UDPSender:
    def __init__(self, config_obj, wrapper=DefaultWrapper()):
        self.config_obj = (config_obj,)
        self.wrapper = wrapper
