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
        db.commit()
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
        '''
        if os.path.exists("musicService.db"):
            os.remove("demofile.txt")
        '''
        with app.open_resource('musicService.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Just some welcome page
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Team Awesome</h1>
<p>A prototype API for a music microservice.</p>'''


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

# What is shown if there is an error
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


#
############################## END OF PLAYLIST MICROSERVICE CODE ######################################
#