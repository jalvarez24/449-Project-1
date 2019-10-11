# Music Microservices APIs
# CPSC 449- Backend Engineering

import flask
import json
from flask import request, jsonify, g, make_response
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


app = flask.Flask(__name__)
app.config.from_envvar('APP_CONFIG')


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = make_dicts
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.cli.command('init')
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('musicService.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Just some welcome page
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Team Awesome</h1>
<p>A prototype API for a music microservice.</p>'''

#
############################## TRACKS MICROSERVICE CODE ########################################
#

# Gets all the tracks from the Track Table and turns it into json
@app.route('/api/v1/resources/musicService/tracks/all', methods=['GET'])
def track_all():
    all_tracks = query_db('SELECT * FROM Track;')

    return jsonify(all_tracks)

# This retrieves a track. This filters the Track table depending on the query
@app.route('/api/v1/resources/musicService/tracks', methods=['GET'])
def api_filter():
    query_parameters = request.args

    track_id = query_parameters.get('track_id')


    if track_id is None:
        return page_not_found(404)

    query = "SELECT * FROM Track WHERE"
    to_filter = []

    if track_id:
        query += ' track_id=? AND'
        to_filter.append(track_id)
    
    if not (track_id):
        return page_not_found(404)

    query = query[:-4] + ';'

    results = query_db(query, to_filter)

    return jsonify(results)

# This allows the user to create a track and POST it to the database
@app.route('/api/v1/resources/musicService/tracks', methods=['POST'])
def create_track():
    conn = sqlite3.connect('musicService.db')
    c = conn.cursor()

    #takes in request (sent in with curl as JSON data)
    # and turn it into python dict. with 'get_json()' function
    input = request.get_json()

    track_title = input['track_title']
    album_title = input['album_title']
    artist = input['artist']
    length_seconds = input['length_seconds']
    url_media = input['url_media']
    url_art = input['url_art']


    params = (track_title, album_title, artist, length_seconds, url_media, url_art)

    c.execute("INSERT INTO Track VALUES(NULL, ?, ?, ?, ?, ?, ?)", params) # This is what worked
    #c.execute("SELECT * FROM Track ORDER BY track_id DESC LIMIT 1")

    # This would query for the track_id

    #setting up response data
    data = jsonify({'response' : 'HTTP 201 Created',
        'code' : '201',
        'posted_title' : track_title,
        'posted_album_title' : album_title,
        'posted_artist' : artist,
        'posted_length' : length_seconds,
        'posted_url_media' : url_media,
        'posted_url_art' : url_art
    })

    conn.commit()
    conn.close()
    #create response to return
    return make_response(data, 201)

@app.route('/api/v1/resources/musicService/tracks', methods=['DELETE'])
def delete_track():
    conn = sqlite3.connect('musicService.db')
    c = conn.cursor()

    input = request.get_json()

    if not 'track_id' in input.keys():
        error = jsonify({'response' : 'HTTP 404, Missing Required Fields',
            'code' : '404',
        })
        return make_response(error, 404)

    track_id = input['track_id']

    #check if track_id in database before deletion
    # "SELECT track_id FROM Track WHERE track_id = 5 "
    c.execute("SELECT track_id FROM Track WHERE track_id = \"" + track_id + "\";")
    found = c.fetchone()

    #track_id already exists, return  HTTP 409 Conflict.
    if found:
        c.execute("DELETE FROM Track WHERE track_id = \"" + track_id + "\";")
        #setting up response data
        data = jsonify({'response' : 'HTTP 200 OK',
            'code' : '200',
        })

        conn.commit()
        conn.close()

        #create response to return
        return make_response(data, 200)

    #if no user found
    return page_not_found(404)

@app.route('/api/v1/resources/musicService/tracks/edit-track', methods=['PUT'])
def edit_track():
    conn = sqlite3.connect('musicService.db')
    c = conn.cursor()

    input = request.get_json()

    if not 'track_id' in input.keys() or not 'newTrackTitle' or not 'newAlbumTitle' or not 'newArtist' or not 'newLength' or not 'newUrlMedia' or not 'newUrlArt' in input.keys():
        error = jsonify({'response' : 'HTTP 404, Missing Required Fields',
            'code' : '404',
        })
        return make_response(error, 404)

    track_id_toUpdate = input['track_id'] 
    newTrackTitle = input['newTrackTitle']
    newAlbumTitle = input['newAlbumTitle']
    newArtist = input['newArtist']
    newLength = input['newLength']
    newUrlMedia = input['newUrlMedia']
    newUrlArt = input['newUrlArt']

    

    #check if track_id in database before deletion
    # "SELECT track_id FROM Track WHERE track_id = 5 "
    c.execute("SELECT track_id FROM Track WHERE track_id = \"" + track_id_toUpdate + "\";")
    found = c.fetchone()

    # edit the track with this id
    # "UPDATE Track SET tite = "?", artist = "?", year = "?"" WHERE track_id = track_id; "
    if found:
        c.execute("UPDATE Track SET track_title = \""       + newTrackTitle  +
                                    "\", album_title = \""  + newAlbumTitle  + 
                                    "\", artist = \""       + newArtist      +
                                  "\", length_seconds = \"" + newLength      +
                                    "\", url_media = \""    + newUrlMedia    + 
                                    "\", url_art = \""      + newUrlArt      +"\" WHERE track_id = \"" + track_id_toUpdate + "\";")
        #setting up response data
        data = jsonify({'response' : 'HTTP 200 OK',
            'code' : '200',
        })

        conn.commit()
        conn.close()

        #create response to return
        return make_response(data, 200)

    #if no user found
    return page_not_found(404)

#
############################## END OF TRACKS MICROSERVICE CODE ########################################
#


#
############################## PLAYLIST MICROSERVICE CODE #############################################
#

### List all playlists
@app.route('/api/v1/resources/musicService/playlists/all', methods=['GET'])
def playlist_all():
    all_playlist = query_db('SELECT * FROM Playlist;')

    return jsonify(all_playlist)

### List all playlists created by particular user
@app.route('/api/v1/resources/musicService/playlists/user', methods=['GET'])
def playlist_filter():
    query_parameters = request.args

    username_id = query_parameters.get('username_id')


    if username_id is None:
        return page_not_found(404)

    query = "SELECT * FROM Playlist WHERE"
    to_filter = []

    if username_id:
        query += ' username_id=? AND'
        to_filter.append(username_id)
    
    if not (username_id):
        return page_not_found(404)

    query = query[:-4] + ';'

    results = query_db(query, to_filter)

    return jsonify(results)


### Create a new playlist
@app.route('/api/v1/resources/musicService/playlists', methods=['POST'])
def create_playlist():
    conn = sqlite3.connect('musicService.db')
    c = conn.cursor()

    #takes in request (sent in with curl as JSON data)
    # and turn it into python dict. with 'get_json()' function
    input = request.get_json()

    playlist_title = input['playlist_title']
    description = input['description']
    username_id = input['username_id']
    


    params = (playlist_title, description, username_id)

    c.execute("INSERT INTO Playlist VALUES(NULL, ?, ?, ?)", params) # This is what worked
    #c.execute("SELECT * FROM Track ORDER BY track_id DESC LIMIT 1")

    # This would query for the track_id

    #setting up response data
    data = jsonify({'response' : 'HTTP 201 Created',
        'code' : '201',
        'posted_playlist_title' : playlist_title,
        'posted_description' : description,
        'posted_username_id' : username_id
    })

    conn.commit()
    conn.close()
    #create response to return
    return make_response(data, 201)


### Retrieve a playlist
@app.route('/api/v1/resources/musicService/playlists', methods=['GET'])
def retrieve_playlist():
    query_parameters = request.args

    playlist_id = query_parameters.get('playlist_id')


    if playlist_id is None:
        return page_not_found(404)

    query = "SELECT * FROM Playlist WHERE"
    to_filter = []

    if playlist_id:
        query += ' playlist_id=? AND'
        to_filter.append(playlist_id)
    
    if not (playlist_id):
        return page_not_found(404)

    query = query[:-4] + ';'

    results = query_db(query, to_filter)

    return jsonify(results)

### Delete a playlist
@app.route('/api/v1/resources/musicService/playlists', methods=['DELETE'])
def delete_playlist():
    conn = sqlite3.connect('musicService.db')
    c = conn.cursor()

    input = request.get_json()

    if not 'playlist_id' in input.keys():
        error = jsonify({'response' : 'HTTP 404, Missing Required Fields',
            'code' : '404',
        })
        return make_response(error, 404)

    playlist_id = input['playlist_id']

    #check if track_id in database before deletion
    # "SELECT track_id FROM Track WHERE track_id = 5 "
    c.execute("SELECT playlist_id FROM Playlist WHERE playlist_id = \"" + playlist_id + "\";")
    found = c.fetchone()

    #track_id already exists, return  HTTP 409 Conflict.
    if found:
        c.execute("DELETE FROM Playlist WHERE playlist_id = \"" + playlist_id + "\";")
        #setting up response data
        data = jsonify({'response' : 'HTTP 200 OK',
            'code' : '200',
        })

        conn.commit()
        conn.close()

        #create response to return
        return make_response(data, 200)

    #if no user found
    return page_not_found(404)



#
############################## END OF PLAYLIST MICROSERVICE CODE ######################################
#


# Jayro Alvarez
# **For reference only! (Not part of project requirements)**
# Get all descriptions from 'description' table
@app.route('/api/v1/resources/musicService/description/all', methods=['GET'])
def description_all():
    all_descriptions = query_db('SELECT * FROM Description;')

    return jsonify(all_descriptions)

#
# USERS MICROSERVICE ROUTES:
#

# Jayro Alvarez
@app.route('/api/v1/resources/musicService/users', methods=['POST'])
def create_user():
    #takes in request (sent in with curl as JSON data)
    # and turn it into python dict. with 'get_json()' function
    input = request.get_json()

    required_fields = ['username', 'password', 'display_name', 'email']
    # if not all required fields inputted return 404
    if not all([field in input for field in required_fields]):
        error = jsonify({'response' : 'HTTP 404, Missing Required Fields',
            'code' : '404',
        })
        return make_response(error, 404)

    username = input['username']
    password = input['password']
    display_name = input['display_name']
    email = input['email']
    #initialize optional data to 'None'
    homepage_url = None
    #check if optional data was sent in, if not, already set to None
    if 'homepage_url' in input:
        homepage_url = input['homepage_url']

    #hash inputted password:
    hashed_pw = generate_password_hash(password)

    params = (username, hashed_pw, display_name, email, homepage_url)

    conn = sqlite3.connect('musicService.db')
    c = conn.cursor()

    #check if username already in database before insertion
    c.execute("SELECT username FROM User WHERE username = \"" + username + "\";")
    found = c.fetchone()

    #username already exists, return  HTTP 409 Conflict.
    if found:
        #setting up response data
        data = jsonify({'response' : 'HTTP 409 Conflict',
            'code' : '409',
        })

        #create response to return
        return make_response(data)

    c.execute("INSERT INTO User VALUES(?,?,?,?,?)", params)

    conn.commit()
    conn.close()

    #setting up response data
    data = jsonify({'response' : 'HTTP 201 Created',
        'code' : '201',
        'location' : 'http://127.0.0.1:5000/api/v1/resources/musicService/users?username=' + username,
    })
    #create response to return
    return make_response(data, 201)

# Jayro Alvarez
@app.route('/api/v1/resources/musicService/users', methods=['GET'])
def retrieve_profile():
    query_parameters = request.args

    username = query_parameters.get('username')

    #check is username is empty => could lead to None type concatenation below
    if username is None:
        return page_not_found(404)

    query = "SELECT * FROM User WHERE username = \"" + username + "\";"
    to_filter = [username]
    result = query_db(query)

    #If no user is found
    if not result:
        return page_not_found(404)

    #pull out 1st entry in query result => contain dict. with all info in user
    result = result[0]

    #get rid of password prior to returning result
    del result['password']

    return jsonify(result)

# Jayro Alvarez
@app.route('/api/v1/resources/musicService/users', methods=['DELETE'])
def delete_user():
    input = request.get_json()

    if not 'username' in input.keys():
        error = jsonify({'response' : 'HTTP 404, Missing Required Fields',
            'code' : '404',
        })
        return make_response(error, 404)

    username = input['username']

    conn = sqlite3.connect('musicService.db')
    c = conn.cursor()

    #check if username in database before deletion
    c.execute("SELECT username FROM User WHERE username = \"" + username + "\";")
    found = c.fetchone()

    #username already exists, return  HTTP 409 Conflict.
    if found:
        c.execute("DELETE FROM User WHERE username = \"" + username + "\";")
        #setting up response data
        data = jsonify({'response' : 'HTTP 200 OK',
            'code' : '200',
        })

        conn.commit()
        conn.close()

        #create response to return
        return make_response(data, 200)

    #if no user found
    return page_not_found(404)

# Jayro Alvarez
@app.route('/api/v1/resources/musicService/users/change-password', methods=['PUT'])
def change_password():
    input = request.get_json()

    if not 'username' in input.keys() or not 'newpassword' in input.keys():
        error = jsonify({'response' : 'HTTP 404, Missing Required Fields',
            'code' : '404',
        })
        return make_response(error, 404)

    username = input['username']

    #hash new password
    new_password = generate_password_hash(input['newpassword'])

    conn = sqlite3.connect('musicService.db')
    c = conn.cursor()

    #check if username in database before deletion
    c.execute("SELECT username FROM User WHERE username = \"" + username + "\";")
    found = c.fetchone()

    #username already exists, return  HTTP 409 Conflict.
    if found:
        c.execute("UPDATE User SET password = \"" + new_password + "\" WHERE username = \"" + username + "\";")
        #setting up response data
        data = jsonify({'response' : 'HTTP 200 OK',
            'code' : '200',
        })

        conn.commit()
        conn.close()

        #create response to return
        return make_response(data, 200)

    #if no user found
    return page_not_found(404)

# Jayro Alvarez
@app.route('/api/v1/resources/musicService/users/authenticate-user', methods=['POST'])
def authenticate_user():
    #takes in request (sent in with curl as JSON data)
    # and turn it into python dict. with 'get_json()' function
    input = request.get_json()

    required_fields = ['username', 'password']
    # if not all required fields inputted return 404
    if not all([field in input for field in required_fields]):
        error = jsonify({'response' : 'HTTP 404, Missing Required Fields',
            'code' : '404',
        })
        return make_response(error, 404)

    username = input['username']
    password = input['password']

    #create db connection
    conn = sqlite3.connect('musicService.db')
    c = conn.cursor()

    query = "SELECT username, password FROM User WHERE username = \"" + username + "\";"
    result = query_db(query)
    conn.commit()
    conn.close()

    #If no user is found, return 404
    if not result:
        error = jsonify({'response' : 'HTTP 404 Not Found',
            'code' : '404',
        })
        return make_response(error, 404)

    #pull out 1st entry in query result => contain dict. with username and password
    result = result[0]

    #check the stored, hashed value in db with passed in parameter
    password_check = check_password_hash(result['password'], password)

    #if check came back true:
    if password_check == True:
        data = jsonify({'response' : 'HTTP 200 OK',
            'code' : '200',
        })

        #create response to return
        return make_response(data, 200)

    #otherwise, return a 404 not found
    error = jsonify({'response' : 'HTTP 404 Not Found',
        'code' : '404',
    })
    return make_response(error, 404)


#
# DESCRIPTIONS MICROSERVICE ROUTES:
#

# Jayro Alvarez
@app.route('/api/v1/resources/musicService/descriptions/set-user-description', methods=['POST'])
def set_user_description():
    return make_response(201);

# Jayro Alvarez
@app.route('/api/v1/resources/musicService/descriptions/get-user-description', methods=['GET'])
def get_user_description():
    return make_response(200);


# What is shown if there is an error
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
