from passlib.apps import custom_app_context

import psycopg2
from psycopg2.extras import DictCursor

conn = psycopg2.connect('dbname=pyeveassets user=pyeveassets', cursor_factory=DictCursor)

def _select_one(sql, *args):
	with conn.cursor() as curs:
		curs.execute(sql, args)
		result = curs.fetchone()
		assert curs.fetchone() is None
	return result

def _execute(sql, *args):
	with conn, conn.cursor() as curs:
		curs.execute(sql, args)

def create_user(username, password):
	hashed = custom_app_context.encrypt(password)
	_execute('INSERT INTO users (username, password) VALUES (%s, %s)', username, hashed)

def check_login(username, password):
	r = _select_one('SELECT user_id, password FROM users WHERE username = %s', username)
	hashed = r['password']
	if not custom_app_context.verify(password, hashed):
		return None
	return r['user_id']

def create_eve_char(char_id, user_id, char_name, token, token_expires, refresh_token):
	_execute('''
			INSERT INTO eve_chars (char_id, user_id, char_name, token, token_expires, refresh_token)
			VALUES (%s, %s, %s, %s, %s, %s)
			''', char_id, user_id, char_name, token, token_expires, refresh_token)
