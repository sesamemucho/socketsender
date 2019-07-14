"""
Tests for `udpsender.sender` module.
"""
import io
import ipaddress
import pprint
import socket
import threading
import time
import sys
import select

import pytest

from udpsender import sender
import logging

logging.basicConfig()

FOO = None

def do_test1(port=None):
    stream = f"""
---
- name: foo
  target_addr: "127.0.0.1"
  target_port: {port}
  frequency: 4
  length: 9
  source: file
  total: 10
  user_data1: "tests/data/a.txt"
- name: boo
  target_addr: "127.0.0.1"
  target_port: {port}
  frequency: 4
  length: 9
  source: file
  total: 10
  delay: 0.125
  user_data1: "tests/data/b.txt"
...
    """
    sender.UDPSender().run(stream)

def do_test2(port=None):
    global FOO
    stream = f"""
---
- name: foo
  target_addr: "127.0.0.1"
  target_port: {port}
  frequency: 2
  length: 9
  source: file
  total: 10
  user_data1: "tests/data/a.txt"
- name: boo
  target_addr: "127.0.0.1"
  target_port: {port}
  frequency: 2
  length: 9
  source: file
  total: 10
  delay: 0.25
  user_data1: "tests/data/b.txt"
...
    """
    FOO = sender.UDPSender()
    FOO.run(stream)

def do_test3(port=None):
    global FOO
    stream = f"""
---
- name: foo
  target_addr: "127.0.0.1"
  target_port: {port}
  frequency: 2
  length: 5
  source: tests.callables.UDPS_Test2
  total: 10
- name: boo
  target_addr: "127.0.0.1"
  target_port: {port}
  frequency: 2
  length: 5
  source: tests.callables.UDPS_Test2
  total: 10
  delay: 0.25
...
    """
    FOO = sender.UDPSender()
    FOO.run(stream)

def test_ok():
    expected_data = (
        b"aaaaaaa0\n",
        b"bbbbbbb0\n",
        b"aaaaaaa1\n",
        b"bbbbbbb1\n",
        b"aaaaaaa2\n",
        b"bbbbbbb2\n",
        b"aaaaaaa3\n",
        b"bbbbbbb3\n",
        b"aaaaaaa4\n",
        b"bbbbbbb4\n",
        b"aaaaaaa5\n",
        b"bbbbbbb5\n",
        b"aaaaaaa6\n",
        b"bbbbbbb6\n",
        b"aaaaaaa7\n",
        b"bbbbbbb7\n",
        b"aaaaaaa8\n",
        b"bbbbbbb8\n",
        b"aaaaaaa9\n",
        b"bbbbbbb9\n",
        )
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 0))

    port = sock.getsockname()[1]
    thr = threading.Thread(target=do_test1, kwargs={'port': port})
    thr.start()

    for i in range(0, 20):
        msg = sock.recv(1024)
        assert msg == expected_data[i]

def test_stop_all():
    expected_data = (
        b"aaaaaaa0\n",
        b"bbbbbbb0\n",
        b"aaaaaaa1\n",
        b"bbbbbbb1\n",
        b"aaaaaaa2\n",
        b"bbbbbbb2\n",
        b"aaaaaaa3\n",
        b"bbbbbbb3\n",
        b"aaaaaaa4\n",
        b"bbbbbbb4\n",
        b"aaaaaaa5\n",
        b"bbbbbbb5\n",
        b"aaaaaaa6\n",
        b"bbbbbbb6\n",
        b"aaaaaaa7\n",
        b"bbbbbbb7\n",
        b"aaaaaaa8\n",
        b"bbbbbbb8\n",
        b"aaaaaaa9\n",
        b"bbbbbbb9\n",
        )
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 0))
    sock.setblocking(0)

    port = sock.getsockname()[1]
    thr = threading.Thread(target=do_test2, kwargs={'port': port})
    thr.start()

    for i in range(0, 5):
        ready = select.select([sock], [], [], 0.5)
        if ready[0]:
            msg = sock.recv(1024)
            assert msg == expected_data[i]
            if i >= 3:
                FOO.stop_all()
        else:
            # Should time out after next call after i == 3
            assert i == 4

def test_source_call_too_long():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 0))

    port = sock.getsockname()[1]
    thr = threading.Thread(target=do_test3, kwargs={'port': port})
    thr.start()

    for i in range(0, 20):
        msg = sock.recv(1024)
        assert msg == b"Hello"
