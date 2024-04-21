from typing import List
from ..scraper import scrape_products
from ..storages.storage_interface import StorageInterface
from ..models import Product
from ..redis_manager import RedisManager
from ..notifications.notification_interface import NotificationInterface

class ProductService:
    def __init__(self, storage: StorageInterface, redis_manager: RedisManager, notifier: NotificationInterface):
        self.storage = storage
        self.redis_manager = redis_manager
        self.notifier = notifier

    async def fetch_and_process_products(self, base_url: str, page_limit: int = 5):
        updated_count = 0
        raw_products = scrape_products(base_url, page_limit)
        for prod in raw_products:
            try:
                product = Product(**prod)
                product_data = product.dict(by_alias=True)
                
                cached_product = await self.redis_manager.get_cached_product(product.title)
                if cached_product and float(cached_product['price']) == product.price:
                    continue
                
                await self.storage.save(product_data)
                await self.redis_manager.cache_product(product.title, product_data)
                updated_count += 1
                
            except Exception as e:
                print(f"Failed to process product {prod}: {e}")

        await self.notifier.send(f"{updated_count} products processed/updated from {base_url}.")
        return {"message": f"{updated_count} products processed/updated from {base_url}."}

