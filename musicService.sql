
PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

DROP TABLE IF EXISTS Tracks_List;
DROP TABLE IF EXISTS Playlist;
DROP TABLE IF EXISTS Description;
DROP TABLE IF EXISTS User;

CREATE TABLE Playlist (
    playlist_id INTEGER primary key,
    playlist_title VARCHAR,
    description VARCHAR,
    username_id VARCHAR,
    FOREIGN KEY (username_id) REFERENCES User(username)
);

CREATE TABLE Tracks_List (
    playlist_id INTEGER,
    track_id TEXT,
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
  description_text VARCHAR NOT NULL,
  FOREIGN KEY (username) REFERENCES User(username),
  FOREIGN KEY (track_id) REFERENCES Track(track_id)
);

COMMIT;
