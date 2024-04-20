from dotenv import load_dotenv
import os

load_dotenv()

def get_storage_config():
    return {
        'type': os.getenv('STORAGE_TYPE', 'postgres'),
        'dsn': os.getenv('DATABASE_URL')
    }
