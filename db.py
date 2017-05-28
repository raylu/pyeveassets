from passlib.apps import custom_app_context

import psycopg2
from psycopg2.extras import DictCursor

conn = psycopg2.connect('dbname=pyeveassets user=pyeveassets', cursor_factory=DictCursor)

def _select(sql, *args):
	with conn.cursor() as curs:
		curs.execute(sql, args)
		while True:
			rows = curs.fetchmany()
			if not rows:
				break
			for row in rows:
				yield row

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
			ON CONFLICT (char_id) DO UPDATE
			SET user_id = %s, char_name = %s, token = %s, token_expires = %s, refresh_token = %s
			''', char_id, user_id, char_name, token, token_expires, refresh_token,
			user_id, char_name, token, token_expires, refresh_token)

def refresh_char(char_id, token, token_expires):
	_execute('''
			UPDATE eve_chars SET token = %s, token_expires = %s
			WHERE char_id = %s
			''', token, token_expires, char_id)

def iter_chars(user_id):
	return _select('SELECT char_id, char_name FROM eve_chars WHERE user_id = %s', user_id)

def get_char(user_id, char_id):
	return _select_one('''
			SELECT char_id, char_name, token, token_expires, refresh_token FROM eve_chars
			WHERE user_id = %s and char_id = %s
			''', user_id, char_id)

def stations(station_ids):
	rows = _select('SELECT "stationID", "stationName" FROM "staStations" WHERE "stationID" IN %s', station_ids)
	mapping = {}
	for row in rows:
		mapping[row['stationID']] = row['stationName']
	return mapping

def types(type_ids):
	rows = _select('SELECT "typeID", "typeName" FROM "invTypes" WHERE "typeID" IN %s', type_ids)
	mapping = {}
	for row in rows:
		mapping[row['typeID']] = row['typeName']
	return mapping
