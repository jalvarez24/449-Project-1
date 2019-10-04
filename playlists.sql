-- $ sqlite3 books.db < sqlite.sql

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS Playlists;
CREATE TABLE Playlists (
    playlist_id VARCHAR primary key,
    creator_account VARCHAR,
    playlist_name VARCHAR,
    description VARCHAR       
);
COMMIT;