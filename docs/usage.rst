========
Usage
========

udpsender sends UDP packets on a schedule. The contents and
destinations are set by customized user class passed in at
initialization (if the default behavior isn't suitable). The schedule
and any data the custom classes might want are read from a
configuration file.


Configuration
=============

With the default behaviors, the configuration file sets the size of a
packet, the destination IP address and port number, and the delay
between packets.

A configuration file consists of 


To use UDP Packet Sender in a project::

	import udpsender
