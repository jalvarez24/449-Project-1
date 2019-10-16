# 449 Project 1: Music Microservices
## Group/Roles:
1. Dev1: Jayro Alvarez
2. Dev2: Ian Alvarez
3. Ops:  Brendan Albert

# To Start Using Our Microservices:
1. Open a terminal in Project Directory
2. Run command: `make init`. This will:
	- Run `flask init` and set up the database schema
	- Run `foreman start` to spin up the four microservices
3. The servers is now running! Go to http://127.0.0.1:5000/ to see full user manual




# Music Microservices
# Things being used:
- Curl
- Flask
- Sqlite3
- json

# Tracks Microservice:
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
- >curl -v -d '{"track_title" : "MYSONG", "album_title": "MYALBUM", "artist" : "BestArtist", "length_seconds" : "201", "url_media" : "wwww.soundcloud.com/thisSong", "url_art" : "wwww.flickr.com/thisImage"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5001/api/v1/resources/musicService/tracks



### To *RETRIEVE* a track from the Tracks Microservice:
1. You need to know the *track_title* of the track being retrieved
- *If the **track_title** is not known, get it by retrieving all of tracks first and finding the necessary track_title*
- **To retrieve all of the tracks in the Tracks Microservice:**
- Example:
- >http://127.0.0.1:5001/api/v1/resources/musicService/tracks/all

2. Query for the *track_title* by adding a "?" at the end of the URL: http://127.0.0.1:5001/api/v1/resources/musicService/tracks to signify the start of a query.
- For example:
- >http://127.0.0.1:5001/api/v1/resources/musicService/tracks?track_title=Under Pressure



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
- >curl -v -d '{"track_title" : "Stan", "artist": "Eminem" , "newTrackTitle" : "NEWSONG", "newAlbumTitle": "NEWESTALBUM", "newArtist" : "NEWBestArtist", "newLength" : "180", "newUrlMedia" : "wwww.soundcloud.com/thisSong", "newUrlArt" : "wwww.flickr.com/thisImage"}' -H "Content-Type: application/json" -X PUT http://127.0.0.1:5001/api/v1/resources/musicService/tracks/edit-track




### To *DELETE* a track
1. Be in the right project directory that has your .py, .sql, .db files
2. Enter a **DELETE** curl command:
- **NOTE: Be sure to *provide* all of the *key* values shown below. The order of the way this is inputed MATTERS.**
- "track_title"

**Example of a curl command to DELETE a track:**
- >curl -v -d '{"track_title" : "Sunflower", "artist": "Post Malone"}' -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5001/api/v1/resources/musicService/tracks




# Playlist Microservice:
### To *CREATE* a playlist
1. Be in the right project directory that has your .py, .sql, .db files
2. Enter a **POST** curl command:
- **NOTE: Be sure to use all of the *key* values shown below. The order of the way this is inputed MATTERS.**
- "playlist_title"
- "description"
- "username_id"

**Example of a curl command to POST a playlist:**
- >curl -v -d '{"playlist_title" : "The Feels Train", "description" : "Curl up and cry.", "username_id" : "ian123"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5003/api/v1/resources/musicService/playlists



### To *RETRIEVE* a playlist from the Playlist Microservice:
1. You need to know the *playlist_title* of the playlist being retrieved
- *If the **playlist_title** is not known, get it by retrieving all of playlists first and finding the necessary playlist_title*
- **To retrieve all of the playlists in the Playlist Microservice:**
- Example:
- >http://127.0.0.1:5003/api/v1/resources/musicService/playlists/all

2. Query for the *playlist_id* by adding a "?" at the end of the URL: http://127.0.0.1:5003/api/v1/resources/musicService/playlists to signify the start of a query.
-For example:
>http://127.0.0.1:5003/api/v1/resources/musicService/playlists?playlist_title=Dance Playlist



### To *DELETE* a playlist
1. Be in the right project directory that has your .py, .sql, .db files
2. Enter a **DELETE** curl command:
- **NOTE: Be sure to *provide* all of the *key* values shown below. The order of the way this is inputed MATTERS.**
- "playlist_title"

**Example of a curl command to DELETE a track:**
- >curl -v -d '{"playlist_title": "The Feels Train"}' -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5003/api/v1/resources/musicService/playlists



### How to list *ALL* playlists in the microservice
1. While Flask is running go to:
- >http://127.0.0.1:5003/api/v1/resources/musicService/playlists/all



### How to list *ALL PLAYLISTS CREATED BY A PARTICULAR USER*
1.While Flask is running go to:
- Example:
- >http://127.0.0.1:5003/api/v1/resources/musicService/playlists/user?username_id=ian123





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

Tracks_List Table:  
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

# Operations

### How to run Procfile
To easily spin up all four microservices, we employ a Procfile.
In the terminal, navigate to the directory containing the Procfile and run:

`foreman start`

### How to add Users via shellscript
Steps:
1. Shell script files must be explicitly given execute permission before they can be run.
To do so, run the following command.
Assume the file name is users.sh.

*Note: permission only needs to be given once per file, then each file that has been given permission can be run as many times as needed.*

`chmod +x users.sh`

2. To add new users to our REST api, we will use a pre-filled shell script.  
To add the users, run the following command:

`./users.sh`
