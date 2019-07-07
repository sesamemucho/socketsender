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
  IPV4 address:port address used as the destination of the UDP packets.

frequency
  In units of packets per second. It may be an integer or the name of
  a function that returns an integer.

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
import logging
import pprint
import re
import sys
import typing

import yaml
from schema import And, Const, Optional, Or, Regex, Schema, Use

from udpsender import callables
from udpsender import exceptions as uexc

MAX_PACKET_SIZE = 65500  # Find a better value, or make it configurable
IPV4_PORT_RE = re.compile(
    r"""\A(
         (?:
            (?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?
            )\.
          ){3}
         (?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)
        )
        :
        (\d{1,5})\Z""",
    re.VERBOSE,
)


def validate_and_extract_ipaddr(s: str) -> typing.Tuple[str, int]:
    mo = IPV4_PORT_RE.match(s)
    if mo:
        return (mo.group(1), int(mo.group(2)))
    else:
        raise uexc.UDPSValueError(f'Can\'t interpret "{s}" as IPV4 addr:port')


builtin_sources = {
    "random": callables.gen_random,
    "sequential": callables.gen_sequential,
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
        self.ip_addr = validated["target_addr"]
        self.frequency = validated["frequency"]
        length = validated["length"]
        if length == "none":
            self.length = None
            # def length_compare(self, ll: typing.Optional[int]) -> bool:
            def length_compare(self, ll: int) -> bool:
                return False

        else:
            self.length = length

            def length_compare(self, ll: int) -> bool:
                return ll < length

        setattr(UDPSSchedule, "length_compare", length_compare)
        self.source = validated["source"]

        total = validated["total"]
        if total == "infinity":
            self.total = None
            # def length_compare(self, ll: typing.Optional[int]) -> bool:
            def total_compare(self, ll: int) -> bool:
                return False

        else:
            self.total = total

            def total_compare(self, ll: int) -> bool:
                return ll < total

        setattr(UDPSSchedule, "total_compare", total_compare)


schema = Schema(
    {
        "name": And(str, len),
        "target_addr": Use(validate_and_extract_ipaddr),
        "frequency": Or(callable, Const(And(Use(int), lambda n: 0 < n))),
        "length": Or("none", And(Use(int), lambda n: 0 < n)),
        "source": Or(Use(to_source), Use(from_callable)),
        "total": Or("infinity", And(Use(int), lambda n: 0 < n)),
        Optional("delay"): And(Or(int, float), Use(float), lambda f: f > 0.0),
    }
)


def get_schedules(stream: typing.TextIO) -> typing.List[UDPSSchedule]:
    max_packet_size = 65500
    data: list = yaml.safe_load(stream)
    return [UDPSSchedule(i) for i in data]
