# -*- coding: utf-8 -*-

"""Provide a pyramid configuration hook."""

import logging
logger = logging.getLogger(__name__)

def includeme(config):
    """Patch the session config with a shared redis connection pool."""
    
    # Unpack.
    registry = config.registry
    settings = registry.settings
    
    # Exit if the session backend isn't redis.
    if settings.get('session.type', None) != 'redis':
        return
    
    # Get a configured redis client.
    from pyramid_redis.hooks import RedisFactory
    redis_factory = RedisFactory()
    redis_client = redis_factory(settings, registry=registry)
    
    # And patch the session settings with its connection pool.
    settings['session.redis_connection_pool'] = redis_client.connection_pool

