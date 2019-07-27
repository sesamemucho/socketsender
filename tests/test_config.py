"""
Tests for `socketsender.config` module.
"""
import ipaddress

import pytest
import schema
from socketsender import callables as udpcalls
from socketsender import config


def test_ok():
    sched = config.get_schedules(
        """
---
- name: foo
  target_addr: "1.1.1.1"
  target_port: 44
  frequency: 1
  length: 100
  source: random
  total: 1000
...
        """
    )

    sch = sched[0]
    assert sch.name == "foo"
    assert sch.tgt_addr == ipaddress.IPv4Address("1.1.1.1")
    assert sch.tgt_port == 44
    assert sch.ip_addr == ("1.1.1.1", 44)
    assert sch.frequency == 1
    assert sch.length == 100
    assert isinstance(sch.source, udpcalls.SOCS_GenRandom)
    assert sch.total == 1000
    assert sch.delay == pytest.approx(0.0)
    assert sch.user_data == dict()

    assert sch.length_compare(99) is True
    assert sch.length_compare(100) is False

    assert sch.total_compare(999) is True
    assert sch.total_compare(1000) is False


def test_source():
    """source can be a callable.
    """
    sched = config.get_schedules(
        """
---
- name: foo
  target_addr: "1.1.1.1"
  target_port: 44
  frequency: 1
  length: 100
  source: tests.callables.SOCS_Test1
  total: 1000
...
        """
    )

    sch = sched[0]
    assert sch.name == "foo"
    assert sch.tgt_addr == ipaddress.IPv4Address("1.1.1.1")
    assert sch.tgt_port == 44
    assert sch.frequency == 1
    assert sch.length == 100
    assert sch.source.__class__.__name__ == "SOCS_Test1"
    assert sch.total == 1000

    assert sch.source() == b"Hello"


def test_length():
    """length can be 'none'
    """
    sched = config.get_schedules(
        """
---
- name: foo
  target_addr: "1.1.1.1"
  target_port: 44
  frequency: 1
  length: none
  source: tests.callables.SOCS_Test1
  total: 1000
...
        """
    )

    sch = sched[0]
    assert sch.name == "foo"
    assert sch.tgt_addr == ipaddress.IPv4Address("1.1.1.1")
    assert sch.tgt_port == 44
    assert sch.frequency == 1
    assert sch.length is None
    assert sch.source.__class__.__name__ == "SOCS_Test1"
    assert sch.total == 1000

    assert sch.length_compare(9999999999999) is False


def test_total():
    """total can be 'infinity'
    """
    sched = config.get_schedules(
        """
---
- name: foo
  target_addr: "1.1.1.1"
  target_port: 44
  frequency: 1
  length: 100
  source: tests.callables.SOCS_Test1
  total: infinity
...
        """
    )

    sch = sched[0]
    assert sch.name == "foo"
    assert sch.tgt_addr == ipaddress.IPv4Address("1.1.1.1")
    assert sch.tgt_port == 44
    assert sch.frequency == 1
    assert sch.length == 100
    assert sch.source.__class__.__name__ == "SOCS_Test1"
    assert sch.total is None

    assert sch.total_compare(9999999999999) is False


def test_delay():
    sched = config.get_schedules(
        """
---
- name: foo
  target_addr: "1.1.1.1"
  target_port: 44
  frequency: 1
  length: 100
  source: random
  total: 1000
  delay: 4.2
...
        """
    )

    sch = sched[0]
    assert sch.name == "foo"
    assert sch.tgt_addr == ipaddress.IPv4Address("1.1.1.1")
    assert sch.tgt_port == 44
    assert sch.frequency == 1
    assert sch.length == 100
    assert isinstance(sch.source, udpcalls.SOCS_GenRandom)
    assert sch.total == 1000
    assert sch.delay == pytest.approx(4.2)

    assert sch.length_compare(99) is True
    assert sch.length_compare(100) is False

    assert sch.total_compare(999) is True
    assert sch.total_compare(1000) is False


def test_ipv6addr():
    sched = config.get_schedules(
        """
---
- name: foo
  target_addr: "2001:db8::1"
  target_port: 44
  frequency: 1
  length: 100
  source: random
  total: 1000
...
        """
    )

    sch = sched[0]
    assert sch.name == "foo"
    assert sch.tgt_addr == ipaddress.IPv6Address("2001:db8::1")
    assert sch.tgt_port == 44


def test_str():
    sched = config.get_schedules(
        """
---
- name: foo
  target_addr: "2001:db8::1"
  target_port: 44
  frequency: 1
  length: 100
  source: random
  total: 1000
  user_data1: yep
  user_data2: nope
...
        """
    )

    sch = sched[0]
    assert (
        f"{sch}"
        == """SOCSchedule "foo" is:
    target_addr: 2001:db8::1
    target_port: 44
    frequency:   1 packets/sec
    length:      100 bytes/packet
    source:      SOCS_GenRandom
    total:       1000 bytes for all packets
    delay:       0.0 sec
    user_data1 is "yep"
    user_data2 is "nope"
"""
    )


def test_str_nouserdata():
    sched = config.get_schedules(
        """
---
- name: foo
  target_addr: "2001:db8::1"
  target_port: 44
  frequency: 1
  length: 100
  source: random
  total: 1000
...
        """
    )

    sch = sched[0]
    assert (
        f"{sch}"
        == """SOCSchedule "foo" is:
    target_addr: 2001:db8::1
    target_port: 44
    frequency:   1 packets/sec
    length:      100 bytes/packet
    source:      SOCS_GenRandom
    total:       1000 bytes for all packets
    delay:       0.0 sec
    No user data has been defined
"""
    )


def test_user_data1():
    sched = config.get_schedules(
        """
---
- name: foo
  target_addr: "1.1.1.1"
  target_port: 44
  frequency: 1
  length: 100
  source: random
  total: 1000
  user_data1: yep
...
        """
    )

    sch = sched[0]
    assert sch.user_data == {"user_data1": "yep"}


def test_user_data2():
    sched = config.get_schedules(
        """
---
- name: foo
  target_addr: "1.1.1.1"
  target_port: 44
  frequency: 1
  length: 100
  source: random
  total: 1000
  user_data2: nope
...
        """
    )

    sch = sched[0]
    assert sch.user_data == {"user_data2": "nope"}


def test_user_data3():
    sched = config.get_schedules(
        """
---
- name: foo
  target_addr: "1.1.1.1"
  target_port: 44
  frequency: 1
  length: 100
  source: random
  total: 1000
  user_data2: satisfactory
  user_data1: pfui!
...
        """
    )

    sch = sched[0]
    assert sch.user_data == {"user_data1": "pfui!", "user_data2": "satisfactory"}


def test_badIP1():
    """The IP Address must be a valid IPV4 address.
    """
    with pytest.raises(schema.SchemaError):
        config.get_schedules(
            """
---
- name: foo
  target_addr: "1.1.1.zoo"
  target_port: 2
  frequency: 1
  length: 100
  source: random
  total: 1000
...
        """
        )


def test_badfrequency():
    """frequency must be a postive number.
    """
    with pytest.raises(schema.SchemaError):
        config.get_schedules(
            """
---
- name: foo
  target_addr: "1.1.1.1"
  target_port: 44
  frequency: -1
  length: 100
  source: random
  total: 1000
...
        """
        )


def test_badlength():
    """length must be a postive number.
    """
    with pytest.raises(schema.SchemaError):
        config.get_schedules(
            """
---
- name: foo
  target_addr: "1.1.1.1"
  target_port: 44
  frequency: 1
  length: 0
  source: random
  total: 1000
...
        """
        )


def test_badsource():
    """source must be a callable or recognized string
    """
    with pytest.raises(schema.SchemaError):
        config.get_schedules(
            """
---
- name: foo
  target_addr: "1.1.1.1"
  target_port: 44
  frequency: 1
  length: 100
  source: wut
  total: 1000
...
        """
        )


def test_badtotal1():
    """total must be 'infinity' or postive number.
    """
    with pytest.raises(schema.SchemaError):
        config.get_schedules(
            """
---
- name: foo
  target_addr: "1.1.1.1"
  target_port: 44
  frequency: 1
  length: 100
  source: random
  total: really_big
...
        """
        )


def test_badtotal2():
    """total must be 'infinity' or postive number.
    """
    with pytest.raises(schema.SchemaError):
        config.get_schedules(
            """
---
- name: foo
  target_addr: "1.1.1.1"
  target_port: 44
  frequency: 1
  length: 100
  source: random
  total: 0
...
        """
        )
