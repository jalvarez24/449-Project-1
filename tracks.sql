-- $ sqlite3 books.db < sqlite.sql

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS Track;
CREATE TABLE Track (
    track_id INTEGER primary key,
    year INT,
    artist VARCHAR,
    title VARCHAR       
);
COMMIT;