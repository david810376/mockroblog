import sys
import textwrap
import logging.config
import sqlite3

import bottle
from bottle import get, post, error, abort, request,delete, response, HTTPResponse
from bottle.ext import sqlite

#set up app and logging
app = bottle.default_app()
app.config.load_config('./etc/timelines.ini')

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

#Routes
#userstimeline
@get('/users/<username>/userTime')
def userstime(db,username):
    usertimeline = query(db, 'SELECT * FROM timelines WHERE username =? ORDER BY time_stamp DESC LIMIT 25',[username])
    response.content_type = 'application/json'
    
    return usertimeline
#publicetimeline
@get('/publicetime')
def publicetime(db):
    publicetimeline = query(db, 'SELECT * FROM timelines ORDER BY time_stamp DESC LIMIT 25')
    response.content_type = 'application/json'
    
    return publicetimeline
#hometimeline
@get('/users/<username>/hometime')
def hometimes(db,username):
    hometimeline = query(db, 'SELECT * FROM timelines WHERE username IN (SELECT follow FROM username WHERE username = ?) ORDER BY time_stamp DESC LIMIT 25', [username])
    response.content_type = 'application/json'
    
    return hometimeline

#post
@post('/users/<username>/tweet')
def user_post(db):
    tweet = request.json
    timestamp = datetime.utcnow()
    if not tweet:
        abort(400)

    posted_fields = tweet.keys()
    #print(posted_fields)
    required_fields = {'username', 'post'}

    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')

    try:
        tweet['id'] = execute(db, '''
        INSERT INTO timelines(username, post, time_stamp)
        VALUES(:username, :post, :timestamp)
        ''', tweet)

    except sqlite3.IntegrityError as e:
        abort(409, str(e))

    response.status = 201
    response.set_header('Location', f"/timelines/{tweet['username']}")
    return tweet
