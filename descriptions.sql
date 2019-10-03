-- $ sqlite3 books.db < sqlite.sql

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS books;
CREATE TABLE books (
    id INTEGER primary key,
    published INT,
    author VARCHAR,
    title VARCHAR,       
    first_sentence VARCHAR,
    UNIQUE(published, author, title)
);
COMMIT;
