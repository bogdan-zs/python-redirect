from flask import (render_template, jsonify, request, redirect)
from urllib.parse import urlparse
import validators
import psycopg2
import re

from app import app, get_db
from .utils import randomString
from .models import link

@app.route('/', methods=['GET'])
def index():
  links = link.all()
  return render_template('index.html', links=links)

INVALID_MESSAGE = 'invalid link'
@app.route('/', methods=['POST'])
def transform_url():
  conn = get_db()
  link_from_user = request.form.get('link')
  if not validators.url(link_from_user):
    return jsonify({'error': INVALID_MESSAGE}), 400
  random_string = randomString()

  try:
    link.save(id=random_string, link=link_from_user)
  except psycopg2.errors.lookup('23505'):
    conn.rollback()
    return transform_url()

  res = { 'link': request.base_url + random_string, 'long_link': link_from_user, 'clicks': 0 }
  return jsonify(res)

DEFAULT_PROTOCOL = 'http://'

@app.route('/<key>')
def redirect_handler(key):
  record = link.get_link_by_key(key)

  if record is None:
    return 'Not Found', 404

  redirect_link = record[0]
  scheme = urlparse(redirect_link).scheme
  if scheme:
    return redirect(redirect_link)
  else:
    return redirect(DEFAULT_PROTOCOL + redirect_link)

@app.errorhandler(500)
def server_error(error):
  conn = get_db()
  conn.rollback()
  return 'Server error', 500