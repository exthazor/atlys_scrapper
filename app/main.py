from fastapi import FastAPI, Depends
from .config import get_storage_config
from .storages.postgres_storage import PostgresStorage
from .services.product_service import ProductService
from .storages.storage_interface import StorageInterface
from .redis_manager import RedisManager

app = FastAPI()

redis_manager = RedisManager()

def get_storage():
    config = get_storage_config()
    return PostgresStorage(config['dsn'])

@app.on_event("startup")
async def startup_event():
    # Initialize Redis or other startup tasks
    pass

@app.on_event("shutdown")
async def shutdown_event():
    await redis_manager.close()

@app.post("/scrape/")
async def add_product(base_url: str, page_limit: int = 5, storage: StorageInterface = Depends(get_storage)):
    product_service = ProductService(storage, redis_manager)
    result = await product_service.fetch_and_process_products(base_url, page_limit)
    return result
