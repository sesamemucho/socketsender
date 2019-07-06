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
  Indicates the number of bytes to send per packet. A value of 'all'
  means to send all the bytes supplied by `source`. Otherwise, it may
  be a positive integer or the name of a function that returns such an
  integer. Will be automatically reduced to maintain `frequency`.

source
  The source of the bytes to send. It may be a special string (see
  below) or the name of a function that returns a bytestring to send.

  random
     A string of random bytes. `length` should be set to some positve
     integer.

  sequential
     Byte N+1 = 1 + byte N. This continues across packets. `length`
     should be set to some positve integer.

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

import yaml
import logging
import pprint
import re
import sys
import typing

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
        raise ValueError(f"Can't interpret \"{s}\" as IPV4 addr:port")

builtin_sources = ('random', 'sequential')

class UDPSSchedule:
    def __init__(self, data: dict) -> None:
        validated = schema.validate(data)
        self.name = validated['name']
        self.ip_addr = validated['target_addr']



from schema import Schema, And, Use, Optional, Regex, Const, Or

schema = Schema({'name': And(str, len),
#                  'target_addr':  Regex(IPV4_PORT_RE),
                  'target_addr':  Use(validate_and_extract_ipaddr),
                  'frequency': Or(Const(And(Use(int), lambda n: 0 < n)), callable),
                  'length': Or('all', And(Use(int), lambda n: 0 < n)),
                  'source': Or(*builtin_sources, callable),
                  'total': Or('infinity', And(Use(int), lambda n: 0 < n)),
                  Optional('delay'): And(Or(int, float), Use(float),
                                         lambda f: f > 0.0)
                  })

def get_schedules(stream: typing.TextIO) -> typing.List[UDPSSchedule]:
    max_packet_size = 65500
    data: list = yaml.safe_load(stream)
    return [UDPSSchedule(i) for i in data]

