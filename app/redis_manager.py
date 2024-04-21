import redis.asyncio as redis
import json

class RedisManager:
    def __init__(self, redis_url):
        self.redis_url = redis_url
        self.redis = None

    async def initialize(self):
        """Initialize the Redis connection."""
        self.redis = redis.Redis.from_url(self.redis_url, decode_responses=True)

    async def get_cached_product(self, product_id):
        """Retrieve the cached product data."""
        product_data = await self.redis.get(f"product:{product_id}")
        if product_data:
            return json.loads(product_data)
        return None

    async def cache_product(self, product_id, product_data):
        """Cache the full product data."""
        await self.redis.set(f"product:{product_id}", json.dumps(product_data))

    async def close(self):
        """Close the Redis connection."""
        await self.redis.wait_closed()
