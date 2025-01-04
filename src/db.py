import asyncpg
import config
from models import feedback

async def get_db_connection():
    return await asyncpg.connect(**config.DB_CONFIG)


