# -*- coding: utf-8 -*-

"""Provide a NamespaceManager and Container that use ``ultramemcached``."""

__all__ = [
    'UltraContainer',
    'UltraNamespaceManager'
]

import logging

try:
    import ultramemcache
except ImportError:
    ultramemcache = None

from beaker.container import Container
from beaker.container import NamespaceManager
from beaker.exceptions import MissingCacheParameter
from beaker.util import verify_directory

from beaker.ext.memcached import MemcachedNamespaceManager
from beaker.ext.memcached import MemcachedContainer

class UltraNamespaceManager(MemcachedNamespaceManager):
    """Provides the :class:`.NamespaceManager` API over the
      ``python-ultramemcached`` client library.
    """
    
    def __new__(cls, *args, **kw):
        return object.__new__(UltraNamespaceManager)
    
    def __init__(self, namespace, url, memcache_module='auto', data_dir=None,
            lock_dir=None, **kw):
        NamespaceManager.__init__(self, namespace)
        if not url:
            raise MissingCacheParameter("url is required")
        if lock_dir:
            self.lock_dir = lock_dir
        elif data_dir:
            self.lock_dir = data_dir + "/container_mcd_lock"
        if self.lock_dir:
            verify_directory(self.lock_dir)
        if ultramemcache is None:
            raise ImportError('`python-ultramemcached` is required.')
        _memcache_module = ultramemcache
        self.mc = MemcachedNamespaceManager.clients.get((memcache_module, url),
                _memcache_module.Client, url.split(';'))
    

class UltraContainer(Container):
    """Container class which invokes :class:`.UltraNamespaceManager`."""
    
    namespace_class = UltraNamespaceManager

