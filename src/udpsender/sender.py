"""Sends UDP packets on a schedule.
"""

import pprint
import typing

from udpsender import config


class UDPSender:
    def __init__(self) -> None:
        pass

    def run(self, stream: typing.TextIO) -> None:
        schedules = config.get_schedules(stream)
        print(f"schedule: {schedules[0]}")
