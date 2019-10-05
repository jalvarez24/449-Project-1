-- $ sqlite3 books.db < sqlite.sql

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS Track;
CREATE TABLE Track (
    track_id INTEGER primary key,
    title VARCHAR, 
    artist VARCHAR,    
    year INTEGER  
          
);
INSERT INTO Track(title, artist, year) VALUES('Under Pressure', 'Queen', 1982);
INSERT INTO Track(title, artist, year) VALUES('Bohemian Rhapsody', 'Queen', 1975);
INSERT INTO Track(title, artist, year) VALUES('Stan', 'Eminem', 2000);
INSERT INTO Track(title, artist, year) VALUES('Killshot', 'Eminem', 2018);

DROP TABLE IF EXISTS Playlists;
CREATE TABLE Playlists (
    playlist_id INTEGER primary key,
    creator_account VARCHAR,
    playlist_name VARCHAR,
    description VARCHAR       
);


INSERT INTO Playlists(creator_account, playlist_name, description) VALUES('noobmaster69', 'Tables are Hard', 'When the times are tough');
COMMIT;