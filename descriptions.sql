-- $ sqlite3 books.db < sqlite.sql

PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS Description;
CREATE TABLE Description (
  username VARCHAR PRIMARY KEY,
  track_id INTEGER,
  description_text VARCHAR
);
INSERT INTO Description(username, track_id, description_text)
  VALUES('noobmaster69', 1, 'Wow, what a lit track!');

COMMIT;
