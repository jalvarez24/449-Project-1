-- $ sqlite3 books.db < sqlite.sql

PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS User;
CREATE TABLE User (
  username VARCHAR PRIMARY KEY,
  password VARCHAR,
  display_name VARCHAR,
  email VARCHAR,
  homepage_url VARCHAR,
  UNIQUE(username, email)
);
INSERT INTO User(username, password, display_name, email, homepage_url)
  VALUES('noobmaster69', 'mySecretPassword', 'noooob', 'thegreatnoob@gmail.com', 'https://thenoob.com');

DROP TABLE IF EXISTS Description;
CREATE TABLE Description (
  username VARCHAR PRIMARY KEY,
  track_id INTEGER,
  description_text VARCHAR
);
INSERT INTO Description(username, track_id, description_text)
  VALUES('noobmaster69', 1, 'Wow, what a lit track!');

COMMIT;
