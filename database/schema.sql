DROP TABLE IF EXISTS medication_table;

CREATE TABLE medication_table (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    dose TEXT NOT NULL,
    number_of_items INTEGER NOT NULL
)