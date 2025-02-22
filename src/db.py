import asyncpg
import config
from models import feedback
from datetime import date

async def get_db_connection():
    return await asyncpg.connect(**config.DB_CONFIG)


async def is_feedback_created_today(telegram_id: int) -> bool:
    """Berilgan telegram_id bo'yicha feedback bugun yaratilganmi yoki yo'q?"""
    conn = await asyncpg.connect(**config.DB_CONFIG)
    try:
        query = """
        SELECT created_date::DATE 
        FROM info_feedback 
        WHERE telegram_id = $1 
        ORDER BY created_date DESC 
        LIMIT 1
        """
        row = await conn.fetchrow(query, telegram_id)

        if row:
            feedback_date = row["created_date"]  # Faqat sana qismini olamiz
            return feedback_date == date.today()  # Bugungi sana bilan solishtiramiz
        
        return False  # Agar hech qanday yozuv bo'lmasa, False qaytariladi
    finally:
        await conn.close()