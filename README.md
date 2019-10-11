# 449-Project-1

# Music Microservices

//I think these will already be indexed automatically, so if we want
	//the users to be able to change the order of songs in the playlist_id
	//we might be able to use that, ALTHOUGH, he did not really say that we
	//need to allow the users to edit the playlist
	//he just said create, retrieve, delete, list all pl, and list pl created by user

## Tracks Microservice:


**To retrieve a track from the Tracks Microservice:**
1. You need to know the *track_id* of the track being retrieved
- *If the **track_id** is not known, get it by retrieving all of tracks first and finding then necessary track_id*
-**To retrieve all of the tracks in the Tracks Microservice:**
>http://127.0.0.1:5000/api/v1/resources/musicService/tracks/all

2. Query for the *track_id* by adding a "?" at the end of the URL to signify the start of a query.
-For example:
>http://127.0.0.1:5000/api/v1/resources/musicService/tracks?track_id=1

**To filter with more attributes separate query by &**

Example of filtering with **_multiple_** attributes:
>127.0.0.1:5000/api/v1/resources/musicService/tracks?artist=Queen&year=1982



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
