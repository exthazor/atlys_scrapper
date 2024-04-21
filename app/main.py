from fastapi import FastAPI, Depends
from .config import get_storage_config, get_redis_url
from .services.product_service import ProductService
from .storages.storage_interface import StorageInterface
from .redis_manager import RedisManager
from .notifications import ConsoleNotification

app = FastAPI()

redis_manager = RedisManager()

# Instantiate RedisManager with URL from config
redis_manager = RedisManager(get_redis_url())

@app.on_event("startup")
async def startup_event():
    # Initialize Redis
    await redis_manager.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    # Close Redis connection
    await redis_manager.close()

@app.post("/scrape/")
async def add_product(base_url: str, page_limit: int = 5, storage: StorageInterface = Depends(get_storage_config)):
    notifier = ConsoleNotification()
    product_service = ProductService(storage, redis_manager, notifier)
    result = await product_service.fetch_and_process_products(base_url, page_limit)
    return result
