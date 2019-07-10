"""
Tests for `udpsender.callables` module.
"""
import io
import pprint

import pytest
import schema

from udpsender import callables as udpcalls
from udpsender import config, exceptions


def test_genrandom():
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
    assert sch.source == udpcalls.gen_random

    bstring = sch.source(sch, sch.length)

    assert len(bstring) == 100


def test_genrandom_lenNone():
    sched = config.get_schedules(
        """
---
- name: foo
  target_addr: "1.1.1.1"
  target_port: 44
  frequency: 1
  length: none
  source: random
  total: 1000
...
        """
    )

    sch = sched[0]
    assert sch.source == udpcalls.gen_random

    bstring = sch.source(sch, sch.length)

    assert len(bstring) == 128


def test_gensequential():
    sched = config.get_schedules(
        """
---
- name: foo
  target_addr: "1.1.1.1"
  target_port: 44
  frequency: 1
  length: 140
  source: sequential
  total: 1000
...
        """
    )

    sch = sched[0]
    assert isinstance(sch.source, udpcalls.UDPS_SequentialSource)

    bstring = sch.source(sch, sch.length)

    assert len(bstring) == 140


def test_gensequential_lenNone():
    sched = config.get_schedules(
        """
---
- name: foo
  target_addr: "1.1.1.1"
  target_port: 44
  frequency: 1
  length: none
  source: sequential
  total: 1000
...
        """
    )

    sch = sched[0]
    assert isinstance(sch.source, udpcalls.UDPS_SequentialSource)

    bstring = sch.source(sch, sch.length)

    assert len(bstring) == 128
