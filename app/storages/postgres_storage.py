from app.storages.storage_interface import StorageInterface
import asyncpg

class PostgresStorage(StorageInterface):
    def __init__(self, dsn):
        self.dsn = dsn

    async def save(self, data):
        conn = await asyncpg.connect(self.dsn)
        await conn.execute('''
            insert into products (product_title, product_price, path_to_image)
            values ($1, $2, $3)
            on conflict (product_title) do update
            set product_price = excluded.product_price, path_to_image = excluded.path_to_image
        ''', data['product_title'], data['product_price'], data['path_to_image'])
        await conn.close()

    async def load(self):
        conn = await asyncpg.connect(self.dsn)
        rows = await conn.fetch('select * from products')
        await conn.close()
        return rows
