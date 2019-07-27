"""
Tests for `socketsender.callables` module.
"""
import io
import pprint

import pytest
import schema

from socketsender import callables as udpcalls
from socketsender import config, exceptions


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
    assert isinstance(sch.source, udpcalls.SOCS_GenRandom)

    bstring = sch.source()

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
    assert isinstance(sch.source, udpcalls.SOCS_GenRandom)

    bstring = sch.source()

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
    assert isinstance(sch.source, udpcalls.SOCS_SequentialSource)

    bstring = sch.source()

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
    assert isinstance(sch.source, udpcalls.SOCS_SequentialSource)

    bstring = sch.source()

    assert len(bstring) == 128

def test_genfilesource():
    sched = config.get_schedules(
        """
---
- name: foo
  target_addr: "1.1.1.1"
  target_port: 44
  frequency: 1
  length: 10
  source: file
  total: 1000
  user_data1: "tests/data/a.txt"
...
        """
    )

    sch = sched[0]
    assert isinstance(sch.source, udpcalls.SOCS_FileSource)

    bstring = sch.source()

    assert len(bstring) == 10


def test_genfilesource_lenNone():
    sched = config.get_schedules(
        """
---
- name: foo
  target_addr: "1.1.1.1"
  target_port: 44
  frequency: 1
  length: none
  source: file
  total: 1000
  user_data1: "tests/data/a.txt"
...
        """
    )

    sch = sched[0]
    assert isinstance(sch.source, udpcalls.SOCS_FileSource)

    bstring = sch.source()

    assert len(bstring) == 128


