from app.storages.storage_interface import StorageInterface
import asyncpg

class PostgresStorage(StorageInterface):
    def __init__(self, dsn):
        self.dsn = dsn

    async def save(self, data):
        conn = await asyncpg.connect(self.dsn)
        await conn.execute('''
            INSERT INTO products (product_title, product_price, path_to_image) VALUES ($1, $2, $3)
        ''', data['product_title'], data['product_price'], data['path_to_image'])
        await conn.close()

    async def load(self):
        conn = await asyncpg.connect(self.dsn)
        rows = await conn.fetch('SELECT * FROM products')
        await conn.close()
        return rows
