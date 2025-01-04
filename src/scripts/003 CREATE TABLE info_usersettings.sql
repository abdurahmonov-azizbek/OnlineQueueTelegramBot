CREATE TABLE info_usersettings(
    id SERIAL PRIMARY KEY NOT NULL,
    telegram_id BIGINT NOT NULL UNIQUE,
    language_id INT REFERENCES enum_language(id)
);