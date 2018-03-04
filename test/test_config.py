"""
Tests for `udpsender.config` module.
"""
import io
import pytest

from udpsender import config
from udpsender import exceptions

def test_no_lines():
  """An empty config file should produce a null config
  """
  cfgfile = io.StringIO("")
  lst = list(config.UDPSConfigReader(cfgfile))

  assert(len(lst) == 0)

def test_short_line():
  """There must be at least four items in a line.
  """
  cf = io.StringIO("1 2 3")
  with pytest.raises(exceptions.UDPSException):
      lst = list(config.UDPSConfigReader(cf))

def test_increasing_id():
  """The ID parameter must be monotonically increasing.
  """
  cf = io.StringIO("\n".join(("1 2 3 1.1.1.1:44",
                              "2 2 3 1.1.1.1:44",
                                "2 2 3 1.1.1.1:44")))
  with pytest.raises(exceptions.UDPSException):
      lst = list(config.UDPSConfigReader(cf))

@pytest.mark.parametrize('delay',
                         [-1,
                         -33])
def test_negative_delay(delay):
  """The delay parameter must not be negative
  """
  cf = io.StringIO(f"1 {delay} 3 1.1.1.1:44\n")

  with pytest.raises(exceptions.UDPSException):
      lst = list(config.UDPSConfigReader(cf))

@pytest.mark.parametrize('size',
                         [-1,
                          0,
                         1000000000])
def test_bad_size(size):
  """The size parameter must be positive and sane.
  """
  cf = io.StringIO(f"1 2 {size} 1.1.1.1:44\n")

  with pytest.raises(exceptions.UDPSException):
      lst = list(config.UDPSConfigReader(cf))
