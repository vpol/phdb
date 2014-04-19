# -*- coding: utf-8 -*-
import logging
from beaker.exceptions import InvalidCacheBackendError
import memcache

__author__ = 'Victor Poluksht'

log = logging.getLogger(__name__)

class Cache(dict):
    """Object representing global info cache shared between all projects"""

    def __init__(self, url, prefix, timeout = 0):
        self.mc = memcache.Client([url], debug = 9)
        self.prefix = prefix
        self.timeout = timeout
        if not self.mc.set('x', 'x', 1):
            raise InvalidCacheBackendError('Cannot connect to Memcached')

    def __getitem__(self, key):
        if self.prefix:
            key = self.prefix + str(key)
        return self.mc.get(key)

    def __setitem__(self, key, value, timeout=0):
        if self.prefix:
            key = self.prefix + str(key)
        return self.mc.set(key, value, timeout)

    def __contains__(self, key):
        if self.prefix:
            key = self.prefix + str(key)
        if self.mc.get(key) == None:
            return False
        return True