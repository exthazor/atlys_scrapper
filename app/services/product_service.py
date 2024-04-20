from typing import List
from ..scraper import scrape_products
from ..storages.storage_interface import StorageInterface
from ..models import Product
from ..redis_manager import RedisManager

class ProductService:
    def __init__(self, storage: StorageInterface, redis_manager: RedisManager):
        self.storage = storage
        self.redis_manager = redis_manager

    async def fetch_and_process_products(self, base_url: str, page_limit: int = 5):
        try:
            raw_products = scrape_products(base_url, page_limit)
            for prod in raw_products:
                product = Product(**prod)
                cached_price = await self.redis_manager.get_cached_price(product.title)
                if cached_price is None or float(cached_price) != product.price:
                    await self.storage.save(product.dict())
                    await self.redis_manager.cache_product_price(product.title, product.price)
            return {"message": f"Products processed from {base_url}."}
        except Exception as e:
            return {"error": str(e)}
