# main.py
from fastapi import FastAPI, Depends
from .config import get_storage_config
from .storages.postgres_storage import PostgresStorage
from .services.product_service import ProductService
from .storages.storage_interface import StorageInterface

app = FastAPI()

def get_storage():
    config = get_storage_config()
    if config['type'] == 'postgres':
        return PostgresStorage(config['dsn'])

@app.post("/scrape/")
async def add_product(base_url: str, page_limit: int = 5, storage: StorageInterface = Depends(get_storage)):
    product_service = ProductService(storage)
    result = await product_service.fetch_and_process_products(base_url, page_limit)
    return result
