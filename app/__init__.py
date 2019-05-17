from flask import Flask, g
import psycopg2

import config

app = Flask(__name__)

def connect_db():
  try:
    conn = psycopg2.connect(config.DATABASE_URL)
    return conn
  except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)

def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().execute(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')

from app import routes