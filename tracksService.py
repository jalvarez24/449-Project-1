# Music Microservices APIs
# Ian Michael Jesu Alvarez
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

# What is shown if there is an error
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

#
############################## END OF TRACKS MICROSERVICE CODE ########################################
#