CREATE TABLE enum_language(
    id INT NOT NULL PRIMARY KEY,
    short_name VARCHAR(100),
    full_name VARCHAR(100)
);

INSERT INTO enum_language(id, short_name, full_name)
VALUES
    (1, 'uz', 'Uzbek'),
    (2, 'ru', 'Rus');