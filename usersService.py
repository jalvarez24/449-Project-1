import flask
import json
from flask import request, jsonify, g, make_response
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = flask.Flask(__name__)
#gets the name of the database
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

# What is shown if there is an error
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

#
############################## Jayro Alvarez #############################################
#

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

@app.route('/api/v1/resources/musicService/users', methods=['GET'])
def retrieve_profile():
    input = request.get_json()

    if not 'username' in input.keys():
        error = jsonify({'response' : 'HTTP 404, Missing Required Fields',
            'code' : '404',
        })
        return make_response(error, 404)

    username = input['username']
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
############################## END OF User MICROSERVICE CODE ######################################
#
