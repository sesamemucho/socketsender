"""Reads updsender config file

Everything after a '#' is ignored.
Blank lines are ignored.

The rest of the file consists of lines with the following fields, at minium:

id   (int)
delay;      Time to wait (in milliseconds) after the last packet was sent.
size:       Size of the packet in bytes
dest_addr   Destination address (IPV4:port)

More fields may be consumed by a config plugin.

"""

from typing import NamedTuple
import collections.abc
import logging
import pprint
import re
import shlex
import sys

from udpsender import exceptions

MAX_PACKET_SIZE = 2048                    # Find a better value, or make it configurable
IPV4_PORT_RE = re.compile(
  r"""\A(
         (?:
            (?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?
            )\.
          ){3}
         (?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)
        )
        :
        (\d{1,5})\Z""", re.VERBOSE)

class UDPSItem(NamedTuple):
  item_id: int
  delay: int
  size: int
  dest_ip: str
  dest_port: int

def defaultParser(*args):
  return UDPSItem(*args[:5])

class UDPSConfigReader(collections.abc.Generator):
  def __init__(self, f_in, parser=defaultParser):
    self._items = list()
    self._item_index = 0
    self._logger = logging.getLogger(__name__)
    self._logger.setLevel(logging.DEBUG)
    last_id = -1

    for line in f_in:
      line = re.sub(r'#.*', r'', line.strip())
      self._logger.debug(f"Got line \"{line}\"")
      if re.search(r'^\s*$', line):
        continue

      items = shlex.split(line)
      # Check for errors in the first part

      if len(items) < 4:
        raise exceptions.UDPSException(
          "Need at least four items in configuration line")

      item_id = int(items[0])
      delay = int(items[1])
      size = int(items[2])

      self._logger.debug(f"item_id: {item_id}, last_id: {last_id} delay: {delay}, size: {size}")
      if item_id <= last_id:
        raise exceptions.UDPSValueError(
          f"Item IDs must be monotonically increasing. Got \"{item_id}\", must be greater than \"{last_id}\"")

      last_id = item_id

      if delay < 0:
        raise exceptions.UDPSValueError(
          f"Delay ({delay}) must be positive.")

      if size <= 0 or size > MAX_PACKET_SIZE:
        raise exceptions.UDPSValueError(
          f"size must be positive and less than maximum packet size {MAX_PACKET_SIZE}")

      mo = re.search(
        IPV4_PORT_RE,
        items[3])

      if mo:
        dest_ip = mo.group(1)
        dest_port = int(mo.group(2))
        if dest_port > 65535:
          raise exceptions.UDPSValueError(
            f"Destination port ({dest_port}) must be a valid port number")
      else:
        raise exceptions.UDPSValueError(
          f"Invalid IPv4 address {dest_ip}")

      self._items.append(parser(item_id,
                                delay,
                                size,
                                dest_ip,
                                dest_port,
                                items[5:]))


  def send(self, _):
    try:
      result = self._items[self._item_index]
      self._item_index += 1
    except:
      self.throw()

    return result

  def throw(self, type=None, value=None):
    raise StopIteration

if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)

  for i in UDPSConfigReader(open(sys.argv[1], 'r')):
    pprint.pprint(i)
