"""Exceptions for udpsender module
"""


class UDPSException(Exception):
    """Base UDPSender exception"""

    def __init__(self, msg):
        super().__init__(msg)


class UDPSValueError(UDPSException, ValueError):
    def __init__(self, msg):
        super().__init__(msg)
