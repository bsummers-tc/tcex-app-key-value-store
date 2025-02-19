"""TcEx Framework Module"""

# standard library
import atexit
from functools import cached_property

# third-party
import redis


class RedisClient:
    """A shared REDIS client connection using a Connection Pool.

    Initialize a single shared redis.connection.ConnectionPool.
    For a full list of kwargs see https://redis-py.readthedocs.io/en/latest/#redis.Connection.

    Args:
        host: The Redis host. Defaults to localhost.
        port: The Redis port. Defaults to 6379.
        db: The Redis db. Defaults to 0.
        errors (str, kwargs): The REDIS errors policy (e.g. strict).
        max_connections (int, kwargs): The maximum number of connections to REDIS.
        password (str, kwargs): The REDIS password.
        socket_timeout (int, kwargs): The REDIS socket timeout.
        timeout (int, kwargs): The REDIS Blocking Connection Pool timeout value.
    """

    _instances = []

    def __init__(
        self,
        host: str = 'localhost',
        port: int = 6379,
        db: int = 0,
        **kwargs,
    ):
        """Initialize class properties"""
        self.pool = redis.ConnectionPool(host=host, port=port, db=db, **kwargs)
        self._instances.append(self)

    @cached_property
    def client(self) -> redis.Redis:
        """Return an instance of redis.client.Redis."""
        return redis.Redis(connection_pool=self.pool)

    @atexit.register
    @staticmethod
    def close():
        """Close the Redis connection pool."""
        for instance in RedisClient._instances:
            instance.pool.disconnect()
            instance.client.close()
