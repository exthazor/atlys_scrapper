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
        try:
            raw_products = scrape_products(base_url, page_limit)
            for prod in raw_products:
                try:
                    product = Product(**prod)
                    cached_price = await self.redis_manager.get_cached_price(product.title)
                    if cached_price is None or float(cached_price) != product.price:
                        await self.storage.save(product.dict(by_alias=True))
                        await self.redis_manager.cache_product_price(product.title, product.price)
                        updated_count += 1
                except Exception as e:
                    print(f"Failed to process product {prod}: {e}")
            await self.notifier.send(f"{updated_count} products processed/updated from {base_url}.")
            return {"message": f"{updated_count} products processed from {base_url}."}
        except Exception as e:
            error_message = f"Error processing products from {base_url}: {str(e)}"
            await self.notifier.send(error_message)
            return {"error": str(e)}
