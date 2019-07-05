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

target_ip
  IP address used to construct target address.

target_port
  Port number used to construct target address.

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

from udpsender import exceptions

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


class UDPSConfig():
    max_packet_size: int = 65500

    def __init__(self, stream: typing.TextIO) -> None:
        pass
