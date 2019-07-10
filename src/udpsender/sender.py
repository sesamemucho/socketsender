"""Sends UDP packets on a schedule.
"""

import datetime
import threading
import time
import typing

from udpsender import config

class UDPSrunner(threading.Thread):
    def __init__(self,
                run_request: threading.Event,
                schedule: config.UDPSSchedule):

        super().__init__(name=schedule.name)
        self.schedule = schedule
        self.run_request = run_request
        self.quitquit = threading.Event()

    def quit(self):
        self.quitquit.set()

    def run(self):
        self.run_request.wait()
        this_time = datetime.datetime.utcnow()
        i = 0
        time.sleep(self.schedule.delay)
        while not self.quitquit.is_set():
            print(f"Hello from {self.name}")
            i += 1
            if i >= 5:
                self.quitquit.set()

class UDPSender:
    def __init__(self) -> None:
        pass

    def run(self, stream: typing.TextIO) -> None:
        schedules = config.get_schedules(stream)
        print(f"schedule: {schedules[0]}")
        syncthreads = threading.Event()
        sch_threads = list()
        for sched in schedules:
            sth = UDPSrunner(syncthreads, sched)
            sch_threads.append(sth)
            sth.start()

        syncthreads.set()

        for sth in sch_threads:
            sth.join()
