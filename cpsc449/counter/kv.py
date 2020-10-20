# Simple persistent key-value store
#
# Inspired by <https://docs.repl.it/misc/database>
#
#     $ FLASK_APP=kv APP_CONFIG=kv.cfg flask run
#     $ export DB_URL=localhost:5000
#

import shelve

from flask import Flask, g, request, jsonify

app = Flask(__name__)
app.config.from_envvar('APP_CONFIG')

DB = {}


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        backing_store = app.config.get('DBM', ':memory:')
        if backing_store == ':memory:':
            db = DB
        else:
            db = shelve.open(backing_store)
        g._database = db
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        if not isinstance(db, dict):
            db.close()

# Set
# http $DB_URL foo=bar


@app.route('/', methods=['POST'])
def set_key():
    req = request.get_json()
    if not req:
        req = request.form
    for key in req.keys():
        get_db()[key] = req[key]
        print('get db is', get_db())
    return jsonify(req)


@app.route('/getDetails', methods=['GET'])
def get_details():
    details = get_db()
    print("details are", details)
    return details

# Get
# http $DB_URL/foo


@app.route('/<key>', methods=['GET'])
def get_key(key):
    print('get db is get', get_db())
    return jsonify({key: get_db().get(key)})

# Delete
# http DELETE $DB_URL/foo


@app.route('/<key>', methods=['DELETE'])
def delete_key(key):
    print('clicked on delete')
    return jsonify({key: get_db().pop(key, None)})


# List
# http $DB_URL
# http $DB_URL?prefix=f
@app.route('/')
def match():
    keys = get_db().keys()
    prefix = request.args.get('prefix')
    if prefix:
        matches = [k for k in keys if k.startswith(prefix)]
    else:
        matches = list(keys)
    return jsonify({'keys': matches})
