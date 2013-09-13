# -*- coding: utf-8 -*-

"""Provide a NamespaceManager and Container that use [python-binary-memcached][].
  
  [python-binary-memcached]: https://github.com/jaysonsantos/python-binary-memcached
"""

__all__ = [
    'BMemcachedContainer',
    'BMemcachedNamespaceManager'
]

import logging

try:
    import bmemcached
except ImportError:
    bmemcached = None

from beaker.container import Container
from beaker.container import NamespaceManager
from beaker.exceptions import MissingCacheParameter
from beaker.util import verify_directory

from beaker.ext.memcached import MemcachedNamespaceManager
from beaker.ext.memcached import MemcachedContainer

class BMemcachedNamespaceManager(MemcachedNamespaceManager):
    """Provides the :class:`.NamespaceManager` API using the underlying
      ``bmemcached`` client.
    """
    
    def __new__(cls, *args, **kw):
        return object.__new__(BMemcachedNamespaceManager)
    
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
        if bmemcached is None:
            raise ImportError('`bmemcached` is required.')
        auth_args = []
        username = kw.get('username', None)
        password = kw.get('password', None)
        if username:
            auth_args.append(username)
        if password:
            auth_args.append(password)
        
        logging.warn('WFT')
        logging.warn((bmemcached, auth_args))
        
        self.mc = MemcachedNamespaceManager.clients.get((memcache_module, url),
                bmemcached.Client, url.split(';'), *auth_args)
    
    def __getitem__(self, key):
        import logging
        logging.warn(('BMemcachedNamespaceManager.__getitem__', key))
        value = self.mc.get(self._format_key(key))
        logging.warn(value)
        return value
    


class BMemcachedContainer(Container):
    """Container class which invokes :class:`.BMemcachedNamespaceManager`."""
    
    namespace_class = BMemcachedNamespaceManager
