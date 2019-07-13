"""

Configuration
=============

With the default behaviors, the configuration file sets the size of a
packet, the destination IP address and port number, and the delay
between packets.

A configuration file is written in a YAML format and sets the
following properties:

name
  The name of this schedule. It is used in reporting,

target_addr
  IP address address used as the destination of the UDP packets.

target_port
  IP port number used as the destination of the UDP packets.

frequency
  In units of packets per second. It may be a floating point or the name of
  a function that returns a floating point.

length
  Indicates the number of bytes to send per packet. A value of 'none'
  means to send all the bytes supplied by `source`. Otherwise, it may
  be a positive integer or the name of a function that returns such an
  integer. Will be automatically reduced to maintain `frequency`.

source
  The source of the bytes to send. It may be a special string (see
  below) or the name of a function that returns a bytestring to send.

  random
     A string of `length` random bytes. If `length` is 'none', this
     function will return 128 byte bytestrings.

  sequential
     Byte N+1 = 1 + byte N, for `length` bytes. This continues across
     packets. If `length` is 'none', this function will return 128
     byte bytestrings.

total
  In units of packets. It may be an integer or the name of a function
  that returns an integer. It may also be 'infinity', which means that
  the sending will continue indefinitely.

delay
  Seconds until transmissions start (floating point). If not present,
  the value defaults to 0.0.

The following properties may be implemented later:

spacing
  Seconds between packets (floating point). Conflicts with `frequency`.

bandwidth
  Desired bytes per second. Conflicts with `length`.

total
  May also have units of bytes.

"""

import importlib
import ipaddress
import re
import typing

import yaml
from schema import And, Const, Optional, Or, Schema, Use

from udpsender import callables
from udpsender import exceptions as uexc

MAX_PACKET_SIZE = 65500  # Find a better value, or make it configurable


builtin_sources = {
    "random": callables.UDPS_GenRandom,
    "sequential": callables.UDPS_SequentialSource,
    "file": callables.UDPS_FileSource
}


def to_source(source_name: str) -> typing.Callable[[int], bytes]:
    """Helper routine to supply functions for the built-in generators.
    """
    return builtin_sources[source_name]


def from_callable(c):
    name, _, func = c.rpartition(".")
    mod = importlib.import_module(name)
    return getattr(mod, func)


class UDPSSchedule:
    def __init__(self, data: dict) -> None:
        """Build a UDPsender Schedule from a configuration section.

        First, we validate using `schema` and a schema.
        Then, we must interpret some of the values.
        """

        validated = schema.validate(data)
        self.name = validated["name"]
        self.tgt_addr = validated["target_addr"]
        self.tgt_port = validated["target_port"]
        self.ip_addr = (str(self.tgt_addr), self.tgt_port)
        self.frequency = validated["frequency"]
        self.length = self.validate_length(validated)
        self.total = self.validate_total(validated)

        if "delay" in validated:
            self.delay = validated["delay"]
        else:
            self.delay = 0.0

        self.user_data = dict()

        if "user_data1" in validated:
            self.user_data["user_data1"] = validated["user_data1"]

        if "user_data2" in validated:
            self.user_data["user_data2"] = validated["user_data2"]

        self.source = validated["source"](self)

    def validate_length(self, schema_data):
        """`length` can have a special value of `none`.
        """
        length = schema_data["length"]
        if length == "none":
            retval = None
            # def length_compare(self, ll: typing.Optional[int]) -> bool:

            def length_compare(_, _x: int) -> bool:
                return False

        else:
            retval = length

            def length_compare(_, current_length: int) -> bool:
                return current_length < length

        setattr(UDPSSchedule, "length_compare", length_compare)

        return retval

    def validate_total(self, schema_data):
        """`total` can have a special value of `infinity`.
        """
        total = schema_data["total"]
        if total == "infinity":
            retval = None
            # def length_compare(self, ll: typing.Optional[int]) -> bool:

            def total_compare(_, _x: int) -> bool:
                return False

        else:
            retval = total

            def total_compare(_, current_total: int) -> bool:
                return current_total < total

        setattr(UDPSSchedule, "total_compare", total_compare)

        return retval


    def __str__(self):
        retval = [f"UDPSchedule \"{self.name}\" is:",
                  f"    target_addr: {self.tgt_addr}",
                  f"    target_port: {self.tgt_port}",
                  f"    frequency:   {self.frequency} packets/sec",
                  f"    length:      {self.length} bytes/packet",
                  f"    source:      {self.source.__class__.__name__}",
                  f"    total:       {self.total} bytes for all packets",
                  f"    delay:       {self.delay} sec"]
        udat = list()
        if "user_data1" in self.user_data:
            udat.append(f"    user_data1 is \"{self.user_data['user_data1']}\"")
        if "user_data2" in self.user_data:
            udat.append(f"    user_data2 is \"{self.user_data['user_data2']}\"")
        if not udat:
            udat.append(f"    No user data has been defined")
        retval.extend(udat)
        return "\n".join(retval) + "\n"

schema = Schema(
    {
        "name": And(str, len),
        "target_addr": Use(ipaddress.ip_address),
        "target_port": And(Use(int), lambda n: 0 <= n <= 65535),
        "frequency": Or(callable, Const(And(Use(float), lambda n: 0 < n))),
        "length": Or("none", And(Use(int), lambda n: 0 < n)),
        "source": Or(Use(to_source), Use(from_callable)),
        "total": Or("infinity", And(Use(int), lambda n: 0 < n)),
        Optional("delay"): And(Or(int, float), Use(float), lambda f: f > 0.0),
        Optional("user_data1"): str,
        Optional("user_data2"): str,
    }
)


def get_schedules(stream: typing.TextIO) -> typing.List[UDPSSchedule]:
    # max_packet_size = 65500
    data: list = yaml.safe_load(stream)
    return [UDPSSchedule(i) for i in data]
