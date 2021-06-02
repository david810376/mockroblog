import sys
import textwrap
import logging.config
import sqlite3

import bottle
from bottle import get, post, error, abort, request,delete, response, HTTPResponse
from bottle.ext import sqlite

#set up app and logging
app = bottle.default_app()
app.config.load_config('./etc/api.ini')

plugin = sqlite.Plugin(app.config['sqlite.dbfile'])
app.install(plugin)



# Return errors in JSON
#
# Adapted from # <https://stackoverflow.com/a/39818780>
#
def json_error_handler(res):
    if res.content_type == 'application/json':
        return res.body
    res.content_type = 'application/json'
    if res.body == 'Unknown Error.':
        res.body = bottle.HTTP_CODES[res.status_code]
    return bottle.json_dumps({'error': res.body})


app.default_error_handler = json_error_handler

# Disable warnings produced by Bottle 0.12.19.
#
#  1. Deprecation warnings for bottle_sqlite
#  2. Resource warnings when reloader=True
#
# See
#  <https://docs.python.org/3/library/warnings.html#overriding-the-default-filter>
#
if not sys.warnoptions:
    import warnings
    for warning in [DeprecationWarning, ResourceWarning]:
        warnings.simplefilter('ignore', warning)


# Simplify DB access
#
# Adapted from
# <https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/#easy-querying>
#
def query(db, sql, args=(), one=False):
    cur = db.execute(sql, args)
    rv = [dict((cur.description[idx][0], value)
          for idx, value in enumerate(row))
          for row in cur.fetchall()]
    cur.close()

    return (rv[0] if rv else None) if one else rv


def execute(db, sql, args=()):
    cur = db.execute(sql, args)
    id = cur.lastrowid
    cur.close()

    return id


# Routes
@get('/')
def home():
    return textwrap.dedent('''
        <h1>Microblog</h1>
    ''')

@get('/users')
def search(db):
    sql = 'SELECT * FROM users'

    columns = []
    values = []

    for column in ['username', 'email', 'password']:
        if column in request.query:
            columns.append(column)
            values.append(request.query[column])

    if columns:
        sql += ' WHERE '
        sql += ' AND '.join([f'{column} = ?' for column in columns])

    logging.debug(sql)
    users = query(db, sql, values)

    return {'users': users}


#create users
#code edit by Professor's code
@post('/users/')
def createuser(db):
    user = request.json

    if not user:
        abort(400)

    posted_fields = user.keys()
    required_fields = {'username', 'email', 'password'}

    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')

    try:
        #post also same type
        user['username'] = execute(db, '''
            INSERT INTO user(username, email, password)
            VALUES(:username, :email, :password)
            ''', user)
    except sqlite3.IntegrityError as e:
        abort(409, str(e))

    response.status = 201
    response.set_header('Location', f"/user/{user['username']}")
    return user

# check password
@get('/users/<username>/password/<password>')
def checkpassword(username,db,password):
     user = query(db, 'SELECT * FROM users WHERE username = ? AND password = ?', [username,password])

     if not user:
        abort(404)

        return {
    'user':user}




#get followers
@get('/users/<username>/followers')
def get_follower(db,username):
    following = query(db, 'SELECT * FROM follow WHERE username = ?', [username])

    if not following:
        abort(404)

    return{'following': following}

#add follower
@post('/users/<username>/followes/<addfollower>')
def follower(db,username):
    addfollow = execute(db, 'INSERT INTO followers(username,followuser) VALUES(:username, :followuser)',addfollow)

    if not addfollow:
        abort(400)

    return {'addfollow':addfollow}
#delete follower
@delete('/users/<username>/followers/<removefollower>')
def deltefollowe(db,username):
    removefollow = execute(db, 'DELETE FROM followers WHERE username = ? AND followuser = ? ', [username,removefollow])

    if not removefollow:
        abort(404)

    return{'removefollow': removefollow}
