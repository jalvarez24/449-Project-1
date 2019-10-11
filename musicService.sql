-- $ sqlite3 books.db < sqlite.sql

PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Playlist;
DROP TABLE IF EXISTS Tracks_List;
DROP TABLE IF EXISTS Description;

CREATE TABLE Track (
    track_id INTEGER PRIMARY KEY,
    track_title VARCHAR,
    album_title VARCHAR,
    artist VARCHAR,
    length_seconds INTEGER,
    url_media VARCHAR,
    url_art VARCHAR,
    UNIQUE(track_title, artist)
);

INSERT INTO Track(track_title, album_title, artist, length_seconds, url_media, url_art) VALUES('Under Pressure', 'Hot Space', 'Queen', 191, 'www.soundcloud.com/songExample1', 'www.www.flickr.com/img1');
INSERT INTO Track(track_title, album_title, artist, length_seconds, url_media, url_art) VALUES('Stan', 'The Marshall Mathers LP','Eminem', 180, 'www.soundcloud.com/songExample2', 'www.www.flickr.com/img2');
INSERT INTO Track(track_title, album_title, artist, length_seconds, url_media, url_art) VALUES('Sunflower', 'Spiderman:Spiderverse', 'Post Malone', 187, 'www.soundcloud.com/songExample3', 'www.www.flickr.com/img3');

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
INSERT INTO User(username, password, display_name, email, homepage_url)
  VALUES('bob42', 'noPass', 'GumsGalore', 'oldDood@gmail.com', 'https://theDood.com');


CREATE TABLE Playlist (
    playlist_id INTEGER PRIMARY KEY,
    playlist_title VARCHAR,
    description VARCHAR,
    username_id VARCHAR
);

INSERT INTO Playlist(playlist_title, description, username_id) VALUES('Tables are Hard', 'When the times are tough', 'noobmaster69');
INSERT INTO Playlist(playlist_title, description, username_id) VALUES('MyPlaylistTitle', '', 'bob42');
INSERT INTO Playlist(playlist_title, description, username_id) VALUES('NewPlaylist', '', 'noobmaster69');


CREATE TABLE Tracks_List (
	list_id INTEGER PRIMARY KEY,
	playlist_id INTEGER,
	track_title VARCHAR
);

INSERT INTO Tracks_List(playlist_id, track_title) VALUES (4, 'Stan');
INSERT INTO Tracks_List(playlist_id, track_title) VALUES (4, 'Sunflower');
INSERT INTO Tracks_List(playlist_id, track_title) VALUES (5, 'Under Pressure');


CREATE TABLE Description (
  username VARCHAR PRIMARY KEY,
  track_id INTEGER,
  description_text VARCHAR
);
INSERT INTO Description(username, track_id, description_text)
  VALUES('noobmaster69', 1, 'Wow, what a lit track!');

COMMIT;
