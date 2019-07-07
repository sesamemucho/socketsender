"""
Tests for `udpsender.config` module.
"""
import io
import pprint

import pytest
import schema

from udpsender import callables as udpcalls
from udpsender import config, exceptions


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
        """
    )

    sch = sched[0]
    assert sch.name == "foo"
    assert sch.ip_addr == ("1.1.1.1", 44)
    assert sch.frequency == 1
    assert sch.length == 100
    assert sch.source == udpcalls.gen_random
    assert sch.total == 1000

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
  target_addr: "1.1.1.1:44"
  frequency: 1
  length: 100
  source: tests.callables.tst1
  total: 1000
...
        """
    )

    sch = sched[0]
    assert sch.name == "foo"
    assert sch.ip_addr == ("1.1.1.1", 44)
    assert sch.frequency == 1
    assert sch.length == 100
    assert sch.source.__name__ == "tst1"
    assert sch.total == 1000

    assert sch.source(sch.length) == b"Hello"


def test_length():
    """length can be 'none'
    """
    sched = config.get_schedules(
        """
---
- name: foo
  target_addr: "1.1.1.1:44"
  frequency: 1
  length: none
  source: tests.callables.tst1
  total: 1000
...
        """
    )

    sch = sched[0]
    assert sch.name == "foo"
    assert sch.ip_addr == ("1.1.1.1", 44)
    assert sch.frequency == 1
    assert sch.length is None
    assert sch.source.__name__ == "tst1"
    assert sch.total == 1000

    assert sch.length_compare(9999999999999) is False


def test_total():
    """total can be 'infinity'
    """
    sched = config.get_schedules(
        """
---
- name: foo
  target_addr: "1.1.1.1:44"
  frequency: 1
  length: 100
  source: tests.callables.tst1
  total: infinity
...
        """
    )

    sch = sched[0]
    assert sch.name == "foo"
    assert sch.ip_addr == ("1.1.1.1", 44)
    assert sch.frequency == 1
    assert sch.length is 100
    assert sch.source.__name__ == "tst1"
    assert sch.total == None

    assert sch.total_compare(9999999999999) is False


def test_badIP1():
    """The IP Address must be a valid IPV4 address.
    """
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
        """
        )


def test_badfrequency():
    """frequency must be a postive number.
    """
    with pytest.raises(schema.SchemaError):
        sched = config.get_schedules(
            """
---
- name: foo
  target_addr: "1.1.1.1:44"
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
        sched = config.get_schedules(
            """
---
- name: foo
  target_addr: "1.1.1.1:44"
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
        sched = config.get_schedules(
            """
---
- name: foo
  target_addr: "1.1.1.1:44"
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
        sched = config.get_schedules(
            """
---
- name: foo
  target_addr: "1.1.1.1:44"
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
        sched = config.get_schedules(
            """
---
- name: foo
  target_addr: "1.1.1.1:44"
  frequency: 1
  length: 100
  source: random
  total: 0
...
        """
        )
