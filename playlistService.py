# Music Microservices APIs
# Ian Michael Jesu Alvarez
# CPSC 449- Backend Engineering

import flask
import json
from flask import request, jsonify, g, make_response, render_template 
import sqlite3


app = flask.Flask(__name__)
app.config.from_envvar('APP_CONFIG')


#called right before any request to establish db connection
#connection saved globally in 'g'
@app.before_request
def connect_to_db():
    g.db = get_db()


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.execute('PRAGMA foreign_keys = ON')
        db.row_factory = make_dicts
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.commit()
        db.close()


@app.errorhandler(404)
def page_not_found(e):
    return jsonify('HTTP 404 Not Found'), 404


@app.errorhandler(409)
def constraint_violation(e):
    return jsonify('HTTP 409 Conflict'), 409




# Just some welcome page
@app.route('/', methods=['GET'])
def home():
    return render_template('user_guide.html')

#
############################## PLAYLIST MICROSERVICE CODE #############################################
#

@app.route('/api/v1/resources/musicService/playlists/all', methods=['GET'])
def playlist_all():

    query = "SELECT * FROM Playlist"
    result = g.db.execute(query)
    found = result.fetchall()

    return make_response(jsonify(found))

### List all playlists created by particular user
@app.route('/api/v1/resources/musicService/playlists/user', methods=['GET'])
def playlist_filter():
    query_parameters = request.args
    username_id = query_parameters.get('username_id')


    if username_id is None:
        return page_not_found(404)

    query = "SELECT * FROM Playlist WHERE username_id = \"" +username_id + "\";"
    result = g.db.execute(query)
    found = result.fetchall()

    if not found:
        return page_not_found(404)

    return make_response(jsonify(found))
    
    
### Create a new playlist
@app.route('/api/v1/resources/musicService/playlists', methods=['POST'])
def create_playlist():
    #takes in request (sent in with curl as JSON data)
    # and turn it into python dict. with 'get_json()' function
    input = request.get_json()

    required_fields = ['playlist_title', 'description', 'username_id']

    if not all([field in input for field in required_fields]):
        return constraint_violation(409)

    playlist_title = input['playlist_title']
    description = None
    username_id = input['username_id']

    #check if optional data was sent in, if not, already set to None
    if 'description' in input:
        description = input['description']
    


    # #if user doesn not exist, they can't create a playlist
    # query = "SELECT * FROM User WHERE user_name = \"" + username_id + "\";"
    # result = g.db.execute(query)
    # found = result.fetchone()

    params = (playlist_title, description, username_id)

    try:
        g.db.execute("INSERT INTO Playlist(playlist_title, description, username_id) VALUES(?, ?, ?)", params) 
    except:
        return constraint_violation(409)

    location = 'http://127.0.0.1:5000/api/v1/resources/musicService/playlists?playlist_title='+ playlist_title

    #  create response to return
    response = make_response(jsonify('New Playlist Created!'), 201)
    response.headers['Location'] = location
    return response


### Retrieve a playlist
@app.route('/api/v1/resources/musicService/playlists', methods=['GET'])
def retrieve_playlist():
    query_parameters = request.args

    playlist_title = query_parameters.get('playlist_title')


    if playlist_title is None:
        return page_not_found(404)

    query = "SELECT * FROM Playlist WHERE playlist_title = \"" + playlist_title +"\";"
    result = g.db.execute(query)
    found = result.fetchone()

    if not found:
        return page_not_found(404)

    return make_response(jsonify(found))

### Delete a playlist
@app.route('/api/v1/resources/musicService/playlists', methods=['DELETE'])
def delete_playlist():
    input = request.get_json()

    if not 'playlist_title' in input.keys():
        return constraint_violation(409)

    playlist_title = input['playlist_title']

    #check if track_id in database before deletion
    # "SELECT track_id FROM Track WHERE track_id = 5 "
    query = "SELECT playlist_title FROM Playlist WHERE playlist_title = \"" + playlist_title + "\";"
    result = g.db.execute(query)
    found = result.fetchone()

    if found:
        delete_user_query = "DELETE FROM Playlist WHERE playlist_title= \"" + playlist_title + "\";"
        #setting up response data
        g.db.execute(delete_user_query)

        response = make_response(jsonify('Playlist deleted'), 200)
        return response

    #if no user found
    return page_not_found(404)

#
############################## END OF PLAYLIST MICROSERVICE CODE ######################################
#