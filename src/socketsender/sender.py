"""Sends IP packets on a schedule.
"""

import logging
import socket
import threading
import time
import typing

from socketsender import config

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class SOCSrunner(threading.Thread):
    def __init__(self, run_request: threading.Event, schedule: config.SOCSSchedule):

        super().__init__(name=schedule.name)
        self.schedule = schedule
        self.name = schedule.name
        self.run_request = run_request
        self.quitquit = threading.Event()
        self.result = dict()
        log.info("hello")

    def stop(self):
        self.quitquit.set()

    def run(self):
        self.run_request.wait()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        period = 1.0 / self.schedule.frequency
        # print(f"{self.name} frequency is {self.schedule.frequency}")
        # print(f"{self.name} period is {period}")
        time.sleep(self.schedule.delay)
        start_time = time.time()
        number_of_packets_sent = 0
        while not self.quitquit.is_set():
            last_time = time.time()
            next_time = last_time + period
            data = self.schedule.source()
            sock.sendto(data, self.schedule.ip_addr)
            number_of_packets_sent += 1
            #            print(f"{self.name} Sent packet {number_of_packets_sent}")
            if number_of_packets_sent >= self.schedule.total:
                break
            wait_time = next_time - time.time()
            #            print(f"{self.name} wait_time is {wait_time}")
            if wait_time > 0.0:
                time.sleep(wait_time)

        self.result["packets"] = number_of_packets_sent
        self.result["time"] = time.time() - start_time
        self.result["frequency"] = (number_of_packets_sent - 1) / self.result["time"]


class SOCSender:
    def __init__(self) -> None:
        self.threads = list()

    def run(self, stream: typing.TextIO) -> None:
        schedules = config.get_schedules(stream)
        syncthreads = threading.Event()
        try:
            for sched in schedules:
                sth = SOCSrunner(syncthreads, sched)
                self.threads.append(sth)
                sth.start()

            syncthreads.set()

            for sth in self.threads:
                sth.join()

        except KeyboardInterrupt:
            self.stop_all()
            for sth in self.threads:
                sth.join()

        # for sth in self.threads:
        #     print(f"frequency for {sth.name} is {pprint.pformat(sth.result)}")

    def stop_all(self):
        for sth in self.threads:
            sth.stop()
