# Music Microservices APIs
# Ian Michael Jesu Alvarez
# CPSC 449- Backend Engineering

import flask
import json
import os
from flask import request, jsonify, g, make_response, render_template 
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


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
############################## TRACKS MICROSERVICE CODE ########################################
#

# Gets all the tracks from the Track Table and turns it into json
@app.route('/api/v1/resources/musicService/tracks/all', methods=['GET'])
def track_all():

    query = "SELECT * FROM Track"
    result = g.db.execute(query)
    found = result.fetchall()

    return make_response(jsonify(found))

# This retrieves a track. This filters the Track table depending on the query
@app.route('/api/v1/resources/musicService/tracks', methods=['GET'])
def api_filter():
    query_parameters = request.args

    track_title = query_parameters.get('track_title')


    if track_title is None:
        return page_not_found(404)

    query = "SELECT * FROM Track WHERE track_title = \"" +track_title + "\";"
    
    result = g.db.execute(query)

    found = result.fetchone()

    if not found:
        return page_not_found(404)


    return make_response(jsonify(found))

# This allows the user to create a track and POST it to the database
@app.route('/api/v1/resources/musicService/tracks', methods=['POST'])
def create_track():
    #takes in request (sent in with curl as JSON data)
    # and turn it into python dict. with 'get_json()' function
    input = request.get_json()

    required_fields = ['track_title', 'album_title', 'artist', 'length_seconds', 'url_media']

    if not all([field in input for field in required_fields]):
        return constraint_violation(409)

    track_title = input['track_title']
    album_title = input['album_title']
    artist = input['artist']
    length_seconds = input['length_seconds']
    url_media = input['url_media']
    url_art = None

    #check if optional data was sent in, if not, already set to None
    if 'url_art' in input:
        url_art = input['url_art']

    query = "SELECT * FROM Track WHERE track_title = \"" + track_title + ", artist = " + artist + "\";"
    result = g.db.execute(query)

    found = result.fetchone()

    if found:
        return constraint_violation(409)

    params = (track_title, album_title, artist, length_seconds, url_media, url_art)
    g.db.execute("INSERT INTO Track VALUES(NULL, ?, ?, ?, ?, ?, ?)", params) # This is what worked
    #c.execute("SELECT * FROM Track ORDER BY track_id DESC LIMIT 1")

    location = 'http://127.0.0.1:5000/api/v1/resources/musicService/tracks?track_title='+track_title
	#create response to return
    response = make_response(jsonify('New Track Created!'), 201)
    response.headers['Location'] = location
    return response

@app.route('/api/v1/resources/musicService/tracks', methods=['DELETE'])
def delete_track():
    input = request.get_json()

    if not 'track_title' in input.keys():
        return constraint_violation(409)

    track_title = input['track_title']

    #check if track_id in database before deletion
    # "SELECT track_id FROM Track WHERE track_id = 5 "
    query = "SELECT track_title FROM Track WHERE track_title = \"" + track_title + "\";"
    result = g.db.execute(query)

    found = result.fetchone()

    #track_id already exists, return  HTTP 409 Conflict.
    if found:
        delete_user_query = "DELETE FROM Track WHERE track_title= \"" + track_title + "\";"
        #setting up response data
        g.db.execute(delete_user_query)

        

        #create response to return
        response = make_response(jsonify('Track deleted'), 200)
        return response

    #if no user found
    return page_not_found(404)

@app.route('/api/v1/resources/musicService/tracks/edit-track', methods=['PUT'])
def edit_track():	

    input = request.get_json()

    if not 'track_title' in input.keys() or not 'artist' or not 'newTrackTitle' or not 'newAlbumTitle' or not 'newArtist' or not 'newLength' or not 'newUrlMedia' or not 'newUrlArt' in input.keys():
        return constraint_violation(409)

    track_title_toUpdate = input['track_title']
    artist_toUpdate = input['artist']  
    newTrackTitle = input['newTrackTitle']
    newAlbumTitle = input['newAlbumTitle']
    newArtist = input['newArtist']
    newLength = input['newLength']
    newUrlMedia = input['newUrlMedia']
    newUrlArt = input['newUrlArt']

    

    #check if track_id in database before deletion
    # "SELECT track_title FROM Track WHERE track_title = Stan AND artist = Eminem "
    query = "SELECT * FROM Track WHERE track_title = \"" + track_title_toUpdate + "\" AND artist = \"" + artist_toUpdate +"\";"
    result = g.db.execute(query)

    found = result.fetchone()

    # edit the track with this id
    # "UPDATE Track SET tite = "?", artist = "?", year = "?"" WHERE track_id = track_id; "
    if found:
        update_query = "UPDATE Track SET track_title = \""  + newTrackTitle  +"\", album_title = \""  + newAlbumTitle  + "\", artist = \"" + newArtist + "\", length_seconds = \"" + newLength +"\", url_media = \"" + newUrlMedia + "\", url_art = \""      + newUrlArt      +"\" WHERE track_title = \"" + track_title_toUpdate + "\" AND artist = \"" + artist_toUpdate +"\";"
        g.db.execute(update_query)
        #setting up response data
        response = make_response(jsonify(track_title_toUpdate + '\'s information was changed!'))

        #create response to return
        return response

    #if no user found
    return page_not_found(404)


# #
# ############################## END OF TRACKS MICROSERVICE CODE ########################################
# #