from fastapi import FastAPI, Depends
from .config import get_storage_config, get_redis_url
from .services.product_service import ProductService
from .storages.postgres_storage import PostgresStorage
from .storages.storage_interface import StorageInterface
from .redis_manager import RedisManager
from .notifications.console_notification import ConsoleNotification

app = FastAPI()

redis_manager = RedisManager(get_redis_url())

@app.on_event("startup")
async def startup_event():
    # Initialize Redis
    await redis_manager.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    # Close Redis connection
    await redis_manager.close()

def get_storage() -> StorageInterface:
    config = get_storage_config()
    return PostgresStorage(config['dsn'])

@app.post("/scrape/dentelstall/")
async def add_product(page_limit: int = 5, storage: StorageInterface = Depends(get_storage)):
    notifier = ConsoleNotification()
    product_service = ProductService(storage, redis_manager, notifier)
    result = await product_service.fetch_and_process_products("https://dentalstall.com/shop/", page_limit)
    return result
