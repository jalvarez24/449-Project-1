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

# Gets all the tracks from the Track Table and turns it into json
@app.route('/api/v1/resources/musicService/tracks/all', methods=['GET'])
def api_all():
    all_books = query_db('SELECT * FROM Track;')

    return jsonify(all_books)

# This filters the Track table depending on the query
@app.route('/api/v1/resources/musicService/tracks', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    artist = query_parameters.get('artist')
    title = query_parameters.get('title')
    track_id = query_parameters.get('track_id')
    year = query_parameters.get('year')

    query = "SELECT * FROM Track WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if artist:
        query += ' artist=? AND'
        to_filter.append(artist)
    if title:
        query += ' title=? AND'
        to_filter.append(title)
    if track_id:
        query += ' track_id=? AND'
        to_filter.append(track_id)
    if year:
        query += ' year=? AND'
        to_filter.append(year)
    if not (id or artist or title or track_id or year):
        return page_not_found(404)

    query = query[:-4] + ';'

    results = query_db(query, to_filter)

    return jsonify(results)

# This allows the user to create a track and POST it to the database
@app.route('/api/v1/resources/musicService/tracks/create-track', methods=['POST'])
def create_track():
    conn = sqlite3.connect('musicService.db')
    c = conn.cursor()

    #takes in request (sent in with curl as JSON data)
    # and turn it into python dict. with 'get_json()' function
    input = request.get_json()

    title = input['title']
    artist = input['artist']
    year = input['year']


    params = (title,artist,year)

    #setting up response data
    data = jsonify({'response' : 'HTTP 201 Created',
        'code' : '201',
        'posted_title' : title,
        'posted_artist' : artist,
        'posted_year' :    year,
    })
    c.execute("INSERT INTO Track VALUES(NULL, ?, ?, ?)", params) # This is what worked

    #These were the tests i was doing:
    #c.execute("INSERT INTO Track VALUES(title, artist, year)")
    #c.execute("INSERT INTO Track VALUES(data["posted_title"], data["posted_artist"], data["posted_year"])")
    #c.execute("INSERT INTO Track VALUES(data.posted_title, data.posted_artist, data.posted_year)")
    #c.execute("INSERT INTO Track(title, artist, year) VALUES(?, ?, ?)", (title, artist, year))
    #c.execute("INSERT INTO Track VALUES(?, ?, ?)", [data["posted_title"], data["posted_artist"], data["posted_year"]])


    conn.commit()
    conn.close()
    #create response to return
    return make_response(data, 201)

# Get all descriptions from 'description' table
@app.route('/api/v1/resources/musicService/description/all', methods=['GET'])
def description_all():
    all_descriptions = query_db('SELECT * FROM Description;')

    return jsonify(all_descriptions)

# Jayro Alvarez
@app.route('/create-user', methods=['POST'])
def create_user():
    conn = sqlite3.connect('musicService.db')
    c = conn.cursor()

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

    c.execute("INSERT INTO User VALUES(?,?,?,?,?)", params)
    conn.commit()
    conn.close()

    #setting up response data
    data = jsonify({'response' : 'HTTP 201 Created',
        'code' : '201',
        'location' : homepage_url,
    })

    #create response to return
    return make_response(data, 201)


# What is shown if there is an error
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
