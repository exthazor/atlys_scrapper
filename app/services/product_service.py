from typing import List
from ..scraper import scrape_products
from ..storages.storage_interface import StorageInterface
from ..models import Product

class ProductService:
    def __init__(self, storage: StorageInterface):
        self.storage = storage

    async def fetch_and_process_products(self, base_url: str, page_limit: int = 5):
        """
        Fetch products from a given URL, validate with Pydantic, and store them in the storage.
        """
        try:
            raw_products = scrape_products(base_url, page_limit)
            products = [Product(title=prod['product_title'],
                                price=float(prod['product_price'].replace('₹', '').replace(',', '').strip()),
                                image_url=prod['path_to_image'])
                        for prod in raw_products]

            for product in products:
                await self.storage.save(product.dict())

            return {"message": f"Successfully processed {len(products)} products from {base_url}."}
        except Exception as e:
            return {"error": str(e)}
