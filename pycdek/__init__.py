from __future__ import absolute_import
from .client import AbstractOrder, AbstractOrderLine, Client
from six.moves import map
VERSION = (0, 3, 1)


def get_version():
    return '.'.join(map(str, VERSION))


__version__ = get_version()

