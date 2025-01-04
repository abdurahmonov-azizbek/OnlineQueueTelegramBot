import db
from models.feedback import Feedback

async def get_all_feedbacks():
    conn = await db.get_db_connection()
    query = "SELECT * FROM info_feedback"

    try:
        rows = await conn.fetch(query)
        feedbacks = [
            Feedback(
                Id = row['id'],
                TelegramId = row['telegram_id'],
                WasRude = row['was_rude'],
                SentToPrivateClinic = row['sent_to_private_clinic'],
                ServiceQuality = row['service_quality'],
                DoctorName = row['doctor_name']
            )
            for row in rows
        ]

        return feedbacks
    except Exception as ex:
        print("[!] Error fetching all feedbacks: {ex}")
        return []
    finally:
        await conn.close()

async def get_feedback_by_id(id: int):
    conn = await db.get_db_connection()
    query = "SELECT * FROM info_feedback WHERE id = $1"

    try:
        row = await conn.fetchrow(query, id)
        if not row:
            print(f"[!] No feedback found with id: {id}")
            return None

        return Feedback(
            Id=row['id'],
            TelegramId=row['telegram_id'],
            WasRude=row['was_rude'],
            SentToPrivateClinic=row['sent_to_private_clinic'],
            ServiceQuality=row['service_quality'],
            DoctorName=row['doctor_name']
        )
    except Exception as ex:
        print(f"[!] Error fetching feedback by id: {ex}")
        return None
    finally:
        await conn.close()

async def get_feedback_by_telegram_id(id: int):
    conn = await db.get_db_connection()
    query = "SELECT * FROM info_feedback WHERE telegram_id = $1"

    try:
        row = await conn.fetchrow(query, id)
        if not row:
            print(f"[!] No feedback found with id: {id}")
            return None

        return Feedback(
            Id=row['id'],
            TelegramId=row['telegram_id'],
            WasRude=row['was_rude'],
            SentToPrivateClinic=row['sent_to_private_clinic'],
            ServiceQuality=row['service_quality'],
            DoctorName=row['doctor_name']
        )
    except Exception as ex:
        print(f"[!] Error fetching feedback by id: {ex}")
        return None
    finally:
        await conn.close()

async def create_feedback(data: dict):
    conn = await db.get_db_connection()
    query = "INSERT INTO info_feedback(telegram_id, was_rude, sent_to_private_clinic, service_quality, doctor_name) VALUES ($1, $2, $3, $4, $5)"

    try:
        await conn.execute(
            query,
            data['TelegramId'],
            data['WasRude'],
            data['SentToPrivateClinic'],
            data['ServiceQuality'],
            data['DoctorName']
        )
    except Exception as ex:
        print(f"[!] Eror with creating feedback: {ex}")
    finally:
        await conn.close()