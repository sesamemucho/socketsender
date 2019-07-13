"""Sends UDP packets on a schedule.
"""

import ipaddress
import socket
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
        i = 0
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        period = 1.0 / self.schedule.frequency

        time.sleep(self.schedule.delay)
        number_of_packets_sent = 0
        while not self.quitquit.is_set():
            last_time = time.time()
            next_time = last_time + period
            data = self.schedule.source()
            sock.sendto(data, self.schedule.ip_addr)
            number_of_packets_sent += 1
            if number_of_packets_sent >= self.schedule.total:
                break
            wait_time = next_time - time.time()
            if wait_time > 0.0:
                time.sleep(wait_time)

class UDPSender:
    def __init__(self) -> None:
        pass

    def run(self, stream: typing.TextIO) -> None:
        schedules = config.get_schedules(stream)
        for sched in schedules:
            print(f"schedule: {sched}")

        syncthreads = threading.Event()
        sch_threads = list()
        for sched in schedules:
            sth = UDPSrunner(syncthreads, sched)
            sch_threads.append(sth)
            sth.start()

        syncthreads.set()

        for sth in sch_threads:
            sth.join()
