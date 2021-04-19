import binascii
import hashlib
import os
import ast
import re
import sys
import uuid
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from functools import wraps

from flask import Flask, g

import config

from config import env,app

from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import Neo4jError
import neo4j.time


DATABASE_USERNAME = env('FB_DATABASE_USERNAME')
DATABASE_PASSWORD = env('FB_DATABASE_PASSWORD')
DATABASE_URL = env('FB_DATABASE_URL')



driver = GraphDatabase.driver(DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD)))





def get_db():
    if not hasattr(g, 'neo4j_db'):
        g.neo4j_db = driver.session()
    return g.neo4j_db




@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'neo4j_db'):
        g.neo4j_db.close()


def set_user(sender, **extra):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        g.user = {'id': None}
        return
    match = re.match(r'^Token (\S+)', auth_header)
    if not match:
        abort(401, 'invalid authorization format. Follow `Token <token>`')
        return
    token = match.group(1)

    def get_user_by_token(tx, token):
        return tx.run(
            '''
            MATCH (user:User {api_key: $api_key}) RETURN user
            ''', {'api_key': token}
        ).single()

    db = get_db()
    result = db.read_transaction(get_user_by_token, token)
    try:
        g.user = result['user']
    except (KeyError, TypeError):
        abort(401, 'invalid authorization key')
    return request_started.connect(set_user, app)
