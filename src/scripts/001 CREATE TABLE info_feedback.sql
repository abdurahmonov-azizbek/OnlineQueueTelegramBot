CREATE TABLE IF NOT EXISTS info_feedback(
    id SERIAL PRIMARY KEY NOT NULL,
    telegram_id BIGINT NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(100),
    was_rude BOOLEAN NOT NULL,
    sent_to_private_clinic BOOLEAN NOT NULL,
    quality_id INT REFERENCES enum_quality(id), -- 1: juda yomon, 2: yomon, 3: yaxshi
    doctor_name VARCHAR(100),
    organization_id INTEGER REFERENCES info_organization(id),
    created_date TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
)