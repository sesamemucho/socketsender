================
IP Packet Sender
================

.. image:: https://badge.fury.io/py/socketsender.png
    :target: http://badge.fury.io/py/socketsender

.. image:: https://travis-ci.com/sesamemucho/socketsender.png?branch=master
    :target: https://travis-ci.com/sesamemucho/socketsender

Send different-sized IP packets to various places on one or more schedules.

I wrote this to help test programs that consume UDP or TCP
data. Without additional code, it is useful for performance
investigations as long as the subject doesn't much care about the
contents of the packets. With custom Python code, the packets can have
whatever data is desired.

Features
--------

The destination, length, frequency, and other characteristics of the
packets are configurable (See :ref:`Configuration` for details).

The capabilities of this package may be accessed either through the
module :py:mod:`socketsender` or through the CLI application of the
same name (:py:mod:`socketsender.app`).
