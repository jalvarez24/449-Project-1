# Music Microservices APIs
# CPSC 449- Backend Engineering
#This file initializes our DB

import flask
import json
from flask import request, jsonify, g, make_response
import sqlite3

app = flask.Flask(__name__)
app.config.from_envvar('APP_CONFIG')

@app.cli.command('init')
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('musicService.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.execute('PRAGMA foreign_key = ON')
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


# Our Home Page/User Documentation Page
@app.route('/', methods=['GET'])
def home():
    return  '''
            <h1>Team Awesome</h1>
            <h2> User Guide for Microservices Application</h2>
            <h3>A prototype API for a music microservice.</h3>
            <p>
                First initialize the database with: <i>flask init</i>
            </p>
            '''