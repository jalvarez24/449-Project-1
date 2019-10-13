
PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

DROP TABLE IF EXISTS Tracks_List;
DROP TABLE IF EXISTS Playlist;
DROP TABLE IF EXISTS Description;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS User;


DROP TABLE IF EXISTS User;


CREATE TABLE Track (
    track_id INTEGER primary key,
    track_title VARCHAR,
    album_title VARCHAR,
    artist VARCHAR,
    length_seconds INTEGER,
    url_media VARCHAR,
    url_art VARCHAR,
    UNIQUE(track_title, artist)
);

CREATE TABLE Playlist (
    playlist_id INTEGER primary key,
    playlist_title VARCHAR,
    description VARCHAR,
    username_id VARCHAR,
    FOREIGN KEY (username_id) REFERENCES User(username)
);

CREATE TABLE Tracks_List (
    playlist_id INTEGER,
    track_id INTEGER,
    FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id),
    FOREIGN KEY (track_id) REFERENCES Track(track_id)
);

CREATE TABLE User (
  username VARCHAR PRIMARY KEY,
  password VARCHAR,
  display_name VARCHAR,
  email VARCHAR,
  homepage_url VARCHAR,
  UNIQUE(username, email)
);

CREATE TABLE Description (
  username VARCHAR NOT NULL,
  track_id INTEGER NOT NULL,
  description_text VARCHAR,
  FOREIGN KEY (username) REFERENCES User(username),
  FOREIGN KEY (track_id) REFERENCES Track(track_id)
);

---------------------------------------------------------------
--SECTION TO INSERT SAMPLE DATA TO START DB WITH--
---------------------------------------------------------------

--Inserting sample tracks
INSERT INTO Track(track_title, album_title, artist, length_seconds, url_media, url_art) VALUES('Under Pressure', 'Hot Space', 'Queen', 191, 'www.soundcloud.com/songExample1', 'www.www.flickr.com/img1');
INSERT INTO Track(track_title, album_title, artist, length_seconds, url_media, url_art) VALUES('Stan', 'The Marshall Mathers LP','Eminem', 180, 'www.soundcloud.com/songExample2', 'www.www.flickr.com/img2');
INSERT INTO Track(track_title, album_title, artist, length_seconds, url_media, url_art) VALUES('Sunflower', 'Spiderman:Spiderverse', 'Post Malone', 187, 'www.soundcloud.com/songExample3', 'www.www.flickr.com/img3');

--Inserting sample users
INSERT INTO User(username, password, display_name, email, homepage_url)
  VALUES('jayro123', 'mySecretPassword', 'jayroAY', 'jayro@gmail.com', 'https://jayro123.com');
INSERT INTO User(username, password, display_name, email, homepage_url)
  VALUES('ian123', 'mySecretPassword', 'ianAY', 'ian@gmail.com', 'https://ian123.com');
INSERT INTO User(username, password, display_name, email, homepage_url)
  VALUES('brendan123', 'mySecretPassword', 'brendanAY', 'brendan@gmail.com', 'https://brendan123.com');

--Inserting sample playlists (Can insert now that there is a user to link to)
INSERT INTO Playlist(playlist_title, description, username_id) VALUES('Chill Playlist', 'For times to chill.', 'jayro123');
INSERT INTO Playlist(playlist_title, description, username_id) VALUES('Dance Playlist', NULL, 'ian123');
INSERT INTO Playlist(playlist_title, description, username_id) VALUES('Fire Playlist', 'It is going down tonight!', 'brendan123');

--Inserting sample tracks intoTracks_List (Can insert now that there are playlists AND tracks to link to)
INSERT INTO Tracks_List(playlist_id, track_id) VALUES(1, 1);
INSERT INTO Tracks_List(playlist_id, track_id) VALUES(2, 2);
INSERT INTO Tracks_List(playlist_id, track_id) VALUES(3, 3);

--Inserting sample descriptions (Can insert now that there are users AND tracks to link to)
INSERT INTO Description(username, track_id, description_text)
  VALUES('jayro123', 1, 'Wow, what a lit track!');
INSERT INTO Description(username, track_id, description_text)
  VALUES('ian123', 2, 'Not bad, not bad.');
INSERT INTO Description(username, track_id, description_text)
  VALUES('brendan123', 3, 'My fave!!! :)');

COMMIT;
