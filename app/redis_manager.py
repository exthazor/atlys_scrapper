import redis.asyncio as redis

class RedisManager:
    def __init__(self, redis_url):
        self.redis_url = redis_url
        self.redis = None

    async def initialize(self):
        """Initialize the Redis connection."""
        self.redis = redis.Redis.from_url(self.redis_url, decode_responses=True)

    async def get_cached_price(self, product_id):
        """Retrieve the cached price for a given product."""
        return await self.redis.get(f"product:{product_id}:price")

    async def cache_product_price(self, product_id, price):
        """Cache the product price."""
        await self.redis.set(f"product:{product_id}:price", price)

    async def close(self):
        """Close the Redis connection."""
        await self.redis.wait_closed()
