PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS Track (
    track_id TEXT primary key,
    track_title VARCHAR,
    album_title VARCHAR,
    artist VARCHAR,
    length_seconds INTEGER,
    url_media VARCHAR,
    url_art VARCHAR,
    UNIQUE(track_title, artist)
);

COMMIT;