CREATE TABLE enum_quality(
                             id INTEGER PRIMARY KEY NOT NULL,
                             short_name VARCHAR(100),
                             full_name VARCHAR(100)
);

INSERT INTO enum_quality(id, short_name, full_name)
VALUES
    (1, 'Juda yomon', 'Juda yomon'),
    (2, 'Yomon', 'Yomon'),
    (3, 'Yaxshi', 'Yaxshi' )