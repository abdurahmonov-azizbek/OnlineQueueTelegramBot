CREATE TABLE IF NOT EXISTS info_feedback(
    id SERIAL PRIMARY KEY NOT NULL,
    telegram_id BIGINT NOT NULL,
    was_rude BOOLEAN NOT NULL,
    sent_to_private_clinic BOOLEAN NOT NULL,
    service_quality INT NOT NULL, -- 1: juda yomon, 2: yomon, 3: yaxshi
    doctor_name VARCHAR(100)
)