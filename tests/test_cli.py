"""
Tests for `socketsender.app.cli` module.
"""
import logging
import os

# import select
# import signal
import socket
import subprocess

# import sys
import tempfile

# import threading

# from multiprocessing import Process
# from socketsender import sender

logging.basicConfig()

FOO = None


def mktemp1(port=None):
    stream = f"""
---
- name: foo
  target_addr: "127.0.0.1"
  target_port: {port}
  frequency: 50
  length: 9
  source: file
  total: 10
  user_data1: "tests/data/a.txt"
- name: boo
  target_addr: "127.0.0.1"
  target_port: {port}
  frequency: 50
  length: 9
  source: file
  total: 10
  delay: 0.01
  user_data1: "tests/data/b.txt"
...
    """
    of, fname = tempfile.mkstemp()
    os.write(of, stream.encode())
    os.close(of)
    return fname


# def do_test2(port=None):
#     global FOO
#     stream = f"""
# ---
# - name: foo
#   target_addr: "127.0.0.1"
#   target_port: {port}
#   frequency: 2
#   length: 9
#   source: file
#   total: 10
#   user_data1: "tests/data/a.txt"
# - name: boo
#   target_addr: "127.0.0.1"
#   target_port: {port}
#   frequency: 2
#   length: 9
#   source: file
#   total: 10
#   delay: 0.25
#   user_data1: "tests/data/b.txt"
# ...
#     """
#     FOO = sender.SOCSender()
#     FOO.run(stream)


# def do_test3(port=None):
#     global FOO
#     stream = f"""
# ---
# - name: foo
#   target_addr: "127.0.0.1"
#   target_port: {port}
#   frequency: 2
#   length: 5
#   source: tests.callables.SOCS_Test2
#   total: 10
# - name: boo
#   target_addr: "127.0.0.1"
#   target_port: {port}
#   frequency: 2
#   length: 5
#   source: tests.callables.SOCS_Test2
#   total: 10
#   delay: 0.25
# ...
#     """
#     FOO = sender.SOCSender()
#     FOO.run(stream)


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
    sock.bind(("", 0))

    port = sock.getsockname()[1]
    fname = mktemp1(port)

    subprocess.Popen(["socketsender", fname], executable="socketsender")

    for i in range(0, 10):
        msg = sock.recv(1024)
        assert msg == expected_data[i]

    os.unlink(fname)


# def test_kbint():
#     """Exercise the Keyboardinterrupt exception in sender.py. If it
#     doesn't hang, it works.
#     """

#     expected_data = (
#         b"aaaaaaa0\n",
#         b"bbbbbbb0\n",
#         b"aaaaaaa1\n",
#         b"bbbbbbb1\n",
#         b"aaaaaaa2\n",
#         b"bbbbbbb2\n",
#         b"aaaaaaa3\n",
#         b"bbbbbbb3\n",
#         b"aaaaaaa4\n",
#         b"bbbbbbb4\n",
#         b"aaaaaaa5\n",
#         b"bbbbbbb5\n",
#         b"aaaaaaa6\n",
#         b"bbbbbbb6\n",
#         b"aaaaaaa7\n",
#         b"bbbbbbb7\n",
#         b"aaaaaaa8\n",
#         b"bbbbbbb8\n",
#         b"aaaaaaa9\n",
#         b"bbbbbbb9\n",
#     )
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     sock.bind(("", 0))

#     port = sock.getsockname()[1]
#     proc = Process(target=do_test1, kwargs={"port": port})
#     proc.start()

#     for i in range(0, 10):
#         msg = sock.recv(1024)
#         assert msg == expected_data[i]

#     os.kill(proc.pid, signal.SIGINT)
#     proc.join()


# def test_stop_all():
#     expected_data = (
#         b"aaaaaaa0\n",
#         b"bbbbbbb0\n",
#         b"aaaaaaa1\n",
#         b"bbbbbbb1\n",
#         b"aaaaaaa2\n",
#         b"bbbbbbb2\n",
#         b"aaaaaaa3\n",
#         b"bbbbbbb3\n",
#         b"aaaaaaa4\n",
#         b"bbbbbbb4\n",
#         b"aaaaaaa5\n",
#         b"bbbbbbb5\n",
#         b"aaaaaaa6\n",
#         b"bbbbbbb6\n",
#         b"aaaaaaa7\n",
#         b"bbbbbbb7\n",
#         b"aaaaaaa8\n",
#         b"bbbbbbb8\n",
#         b"aaaaaaa9\n",
#         b"bbbbbbb9\n",
#     )
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     sock.bind(("", 0))
#     sock.setblocking(0)

#     port = sock.getsockname()[1]
#     thr = threading.Thread(target=do_test2, kwargs={"port": port})
#     thr.start()

#     for i in range(0, 5):
#         ready = select.select([sock], [], [], 0.5)
#         if ready[0]:
#             msg = sock.recv(1024)
#             assert msg == expected_data[i]
#             if i >= 3:
#                 FOO.stop_all()
#         else:
#             # Should time out after next call after i == 3
#             assert i == 4


# def test_source_call_too_long():

#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     sock.bind(("", 0))

#     port = sock.getsockname()[1]
#     thr = threading.Thread(target=do_test3, kwargs={"port": port})
#     thr.start()

#     for i in range(0, 20):
#         msg = sock.recv(1024)
#         assert msg == b"Hello"
