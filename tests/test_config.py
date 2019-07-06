"""
Tests for `udpsender.config` module.
"""
import io
import pprint
import pytest
import schema

from udpsender import config
from udpsender import exceptions

def test_ok():
    sched = config.get_schedules(
    """
---
- name: foo
  target_addr: "1.1.1.1:44"
  frequency: 1
  length: 100
  source: random
  total: 1000
...
        """)

    sch = sched[0]
    assert(sch.name == 'foo')
    assert(sch.ip_addr == ('1.1.1.1', 44))

def test_badIP1():
    with pytest.raises(schema.SchemaError):
        sched = config.get_schedules(
    """
---
- name: foo
  target_addr: "1.1.1.zoo:2"
  frequency: 1
  length: 100
  source: random
  total: 1000
...
        """)

# def test_no_lines():
#   """An empty config file should produce a null config
#   """
#   cfgfile = io.StringIO("")
#   lst = list(config.UDPSConfigReader(cfgfile))

#   assert(len(lst) == 0)

# def test_short_line():
#   """There must be at least four items in a line.
#   """
#   cf = io.StringIO("1 2 3")
#   with pytest.raises(exceptions.UDPSException):
#       lst = list(config.UDPSConfigReader(cf))

# def test_increasing_id():
#   """The ID parameter must be monotonically increasing.
#   """
#   cf = io.StringIO("\n".join(("1 2 3 1.1.1.1:44",
#                               "2 2 3 1.1.1.1:44",
#                                 "2 2 3 1.1.1.1:44")))
#   with pytest.raises(exceptions.UDPSException):
#       lst = list(config.UDPSConfigReader(cf))

# @pytest.mark.parametrize('delay',
#                          [-1,
#                          -33])
# def test_negative_delay(delay):
#   """The delay parameter must not be negative
#   """
#   cf = io.StringIO(f"1 {delay} 3 1.1.1.1:44\n")

#   with pytest.raises(exceptions.UDPSException):
#       lst = list(config.UDPSConfigReader(cf))

# @pytest.mark.parametrize('size',
#                          [-1,
#                           0,
#                          config.MAX_PACKET_SIZE+1])
# def test_bad_size(size):
#   """The size parameter must be positive and sane.
#   """
#   cf = io.StringIO(f"1 2 {size} 1.1.1.1:44\n")

#   with pytest.raises(exceptions.UDPSException):
#       lst = list(config.UDPSConfigReader(cf))

# @pytest.mark.parametrize('ipaddr',
#                          ['1.1.1.300:44',
#                           '1.1.2:44',
#                           '10.20.30.40:444312',
#                           '10.20.30.40:-22',
#                           '1.2.3.4'])
# def test_bad_ipaddr(ipaddr):
#   """The IP Address must look correct, and have a valid port.
#   """
#   cf = io.StringIO(f"1 2 22 {ipaddr}\n")

#   with pytest.raises(exceptions.UDPSException):
#       lst = list(config.UDPSConfigReader(cf))

# def test_good_stuff():
#   """What happens with things work?
#   """
#   cf = io.StringIO("\n".join(("1 20 5 1.2.3.4:44",
#                               "2 30 6 1.1.1.1:444",
#                               "3 40 7 192.168.1.0:4444")))
#   expected = [config.UDPSItem(1, 20, 5, '1.2.3.4', 44),
#               config.UDPSItem(2, 30, 6, '1.1.1.1', 444),
#               config.UDPSItem(3, 40, 7, '192.168.1.0', 4444)]

#   lst = list(config.UDPSConfigReader(cf))
#   assert(expected == lst)

# def test_extra_args():
#   """Make sure we can write a parser that takes extra arguments
#   in the config file.
#   """
#   class UDPStst1(config.UDPSItem):
#     def __init__(self,
#                  item_id: int,
#                  delay: int,
#                  size: int,
#                  dest_ip: str,
#                  dest_port: int,
#                  *args) -> None:
#       super().__init__(item_id, delay, size, dest_ip, dest_port)
#       self.foo = int(args[0])
#       self.boo = int(args[1])

#     def __str__(self):
#       return super().__str__() + f" {self.boo} {self.foo}"

#   def tst1_parser(*args):
#     return UDPStst1(*args)

#   cf = io.StringIO("\n".join(("1 20 5 1.2.3.4:44 88 99",
#                               "2 30 6 1.1.1.1:444 100 200",
#                               "3 40 7 192.168.1.0:4444 400 500")))
#   expected = [UDPStst1(1, 20, 5, '1.2.3.4', 44, 88, 99),
#               UDPStst1(2, 30, 6, '1.1.1.1', 444, 100, 200),
#               UDPStst1(3, 40, 7, '192.168.1.0', 4444, 400, 500)]

#   lst = list(config.UDPSConfigReader(cf, parser=tst1_parser))
#   assert(expected == lst)

