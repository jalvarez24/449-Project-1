# 449-Project-1

# Music Microservices
# Things being used:
- Curl
- Flask
- Sqlite3
- json


//I think these will already be indexed automatically, so if we want
	//the users to be able to change the order of songs in the playlist_id
	//we might be able to use that, ALTHOUGH, he did not really say that we
	//need to allow the users to edit the playlist
	//he just said create, retrieve, delete, list all pl, and list pl created by user

## Tracks Microservice:

### To *CREATE* a track
1. Be in the right project directory that has your .py, .sql, .db files
2. Enter a **POST** curl command:
- **NOTE: Be sure to use all of the *key* values shown below. The order of the way this is inputed MATTERS.**
- "track_title"
- "album_title"
- "artist"
- "length_seconds"
- "url_media"
- "url_art"
**Example of a curl command to POST a track:**
- >curl -d '{"track_title" : "MYSONG", "album_title": "MYALBUM", "artist" : "BestArtist", "length_seconds" : "201", "url_media" : "wwww.soundcloud.com/thisSong", "url_art" : "wwww.flickr.com/thisImage"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/resources/musicService/tracks


### To *RETRIEVE* a track from the Tracks Microservice:
1. You need to know the *track_id* of the track being retrieved
- *If the **track_id** is not known, get it by retrieving all of tracks first and finding the necessary track_id*
- **To retrieve all of the tracks in the Tracks Microservice:**
- Example:
- >http://127.0.0.1:5000/api/v1/resources/musicService/tracks/all

2. Query for the *track_id* by adding a "?" at the end of the URL to signify the start of a query.
-For example:
>http://127.0.0.1:5000/api/v1/resources/musicService/tracks?track_id=1


### To *EDIT* a track
1. Be in the right project directory that has your .py, .sql, .db files
2. Enter a **PUT** curl command:
- **NOTE: Be sure to *provide* all of the *key* values shown below. The order of the way this is inputed MATTERS.**
- "track_id"
- "newTrackTitle"
- "newAlbumTitle"
- "newArtist"
- "newLength"
- "newUrlMedia"
- "newUrlArt"
**Example of a curl command to PUT a track:**
- >curl -d '{"track_id" : "4", "newTrackTitle" : "NEWSONG", "newAlbumTitle": "NEWESTALBUM", "newArtist" : "NEWBestArtist", "newLength" : "180", "newUrlMedia" : "wwww.soundcloud.com/thisSong", "newUrlArt" : "wwww.flickr.com/thisImage"}' -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/api/v1/resources/musicService/tracks/edit-track


### To *DELETE* a track
1. Be in the right project directory that has your .py, .sql, .db files
2. Enter a **DELETE** curl command:
- **NOTE: Be sure to *provide* all of the *key* values shown below. The order of the way this is inputed MATTERS.**
- "track_id"

**Example of a curl command to DELETE a track:**
- >curl -d '{"track_id": "2"}' -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5000/api/v1/resources/musicService/tracks



## Playlist Microservice:

### To *CREATE* a playlist
1. Be in the right project directory that has your .py, .sql, .db files
2. Enter a **POST** curl command:
- **NOTE: Be sure to use all of the *key* values shown below. The order of the way this is inputed MATTERS.**
- "playlist_title"
- "description"
- "username_id"

**Example of a curl command to POST a playlist:**
- >curl -d '{"playlist_title" : "The Feels Train", "description" : "Curl up and cry.", "username_id" : "bob42"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/resources/musicService/playlists


### To *RETRIEVE* a playlist from the Playlist Microservice:
1. You need to know the *playlist_id* of the playlist being retrieved
- *If the **playlist_id** is not known, get it by retrieving all of playlists first and finding the necessary playlist_id*
- **To retrieve all of the playlists in the Playlist Microservice:**
- Example:
- >http://127.0.0.1:5000/api/v1/resources/musicService/playlists/all

2. Query for the *playlist_id* by adding a "?" at the end of the URL to signify the start of a query.
-For example:
>http://127.0.0.1:5000/api/v1/resources/musicService/playlists?playlist_id=1


### To *DELETE* a playlist
1. Be in the right project directory that has your .py, .sql, .db files
2. Enter a **DELETE** curl command:
- **NOTE: Be sure to *provide* all of the *key* values shown below. The order of the way this is inputed MATTERS.**
- "playlist_id"

**Example of a curl command to DELETE a track:**
- >curl -d '{"playlist_id": "3"}' -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5000/api/v1/resources/musicService/playlists


### How to list *ALL* playlists in the microservice
1. While Flask is running go to:
- >http://127.0.0.1:5000/api/v1/resources/musicService/playlists/all


### How to list *ALL PLAYLISTS CREATED BY A PARTICULAR USER*
1.While Flask is running go to:
- Example:
- >http://127.0.0.1:5000/api/v1/resources/musicService/playlists/user?username_id=noobmaster69




Track Table:  
[  
	(PK)"track_id": "0",  
	"title" : "Damn it feels good to be a gangsta",  
	"artist" : "Geto Boys",  
	"year" : "1991"  
]  

Playlists Table:  
[  
	(PK)"playlist_id" : "P1"  
	(FK)"creator_account" : "noobmaster69" //foreign key from the users table, maybe we could just join it as well we'll have to discuss what to do  
	"playlist_name" : "Tables are Hard"  
	"description" : "When the times are tough"  
]  

Playlists_songs Table:  
[  
	(FK)"playlist_id" : "P1"  
	(FK) "track_id" : "0"  
]  

Users Table:  
[  
  (PK)"username" : "noobmaster69"  
  "password" : (save only hashed pw)"pbkdf2:sha1:1000$SVJHC1PEkQsUVziX444uP6eMOQeiIJ7v3PkaL1lY"  
  (defaults to username) "display_name: "John Doe"  
  "email" : "johndoe90@gmail.com"  
  (optional)"homepage_url" : "http://blahblah.com"  
]  

Descriptions Table:  
[  
  (PK)"username" : "noobmaster69"  
  (FK)"track_id" : "1"  
  "description" : "This song was pretty lit!"  
]  
