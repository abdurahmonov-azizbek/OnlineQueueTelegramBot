import db
from models.user_settings import UserSettings

async def get_by_id(id):
    conn = await db.get_db_connection()
    query = "SELECT * FROM info_usersettings WHERE id = $1"

    try:
        row = await conn.fetchrow(query, id)
        if not row:
            print(f"[!] No user settings found with id: {id}")
            return None
        
        return UserSettings(
            Id = row['id'],
            TelegramId = row['telegram_id'],
            LanguageId = row['language_id'],
        )

    except Exception as ex:
        print(f"[!] Error fetching user settings: {ex}")
        return None
    finally:
        await conn.close()

async def get_by_telegram_id(id) -> UserSettings:
    conn = await db.get_db_connection()
    query = "SELECT * FROM info_usersettings WHERE telegram_id = $1"

    try:
        row = await conn.fetchrow(query, id)
        if not row:
            print(f"[!] No user settings found with telegram_id: {id}")
            return None
        
        userSettings = UserSettings(
            Id = row['id'],
            TelegramId = row['telegram_id'],
            LanguageId = row['language_id'],
        )
        
        return userSettings

    except Exception as ex:
        print(f"[!] Error fetching user settings: {ex}")
        return None
    finally:
        await conn.close()

async def get_all():
    conn = await db.get_db_connection()
    query = "SELECT * FROM info_usersettings"

    try:
        rows = await conn.fetch(query)
        usersettings = [
            UserSettings(
                Id = row['id'],
                TelegramId = row['telegram_id'],
                LanguageId = row['language_id']
            )
            for row in rows
        ]

        return usersettings
    except Exception as ex:
        print("[!] Error fetching all user settings: {ex}")
        return []
    finally:
        await conn.close()

async def change(telegram_id, language_id):
    conn = await db.get_db_connection()
    try:
        query = "INSERT INTO info_usersettings(telegram_id, language_id) VALUES ($1, $2)"

        old_usersettings = await get_by_telegram_id(telegram_id)

        if old_usersettings:
            query = "UPDATE info_usersettings SET language_id =$2 WHERE telegram_id = $1"
        
        await conn.execute(query, telegram_id, language_id)
    except Exception as ex:
        print("[!] Error with creating user settings ")
    finally:
        await conn.close()