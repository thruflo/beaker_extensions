"""Provide a pyramid configuration hook."""

# Lazy import so we can import the package when not using this hook.
try:
    from alkey.client import get_redis_client
except ImportError:
    get_redis_client = NotImplemented

def includeme(config, get_redis=None):
    """Patch the session config with a shared redis connection pool."""
    
    # Compose.
    if get_redis is None:
        get_redis = get_redis_client
    
    # Unpack.
    settings = config.registry.settings
    
    # Exit if the session backend isn't redis.
    if settings.get('session.type', None) != 'redis':
        return
    
    # Otherwise make sure we have the dependency.
    if get_redis_client is NotImplemented:
        raise ImportError(u'Could not import `alkey.client.get_redis_client`.')
    
    # Get a configured redis client.
    redis = get_redis(config)
    
    # And patch the session settings with its connection pool.
    settings['session.redis_connection_pool'] = redis.connection_pool

