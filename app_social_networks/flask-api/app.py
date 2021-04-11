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

from flask import Flask, g, request, send_from_directory, abort, request_started,render_template
from flask_restful import Resource, Api, reqparse
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_restful_swagger_2 import Api, swagger, Schema

from flask_json import FlaskJSON, json_response
from flask_cors import CORS

from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import Neo4jError
import neo4j.time



app = Flask(__name__)  # Flask app instance initiated

CORS(app)
FlaskJSON(app)

api = Api(app, title='Neo4j Movie Demo API', api_version='0.0.10')
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Social Network Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})

@api.representation('application/json')
def output_json(data, code, headers=None):
    return json_response(data_=data, headers_=headers, status_=code)

def env(key, default=None, required=True):
    """
    Retrieves environment variables and returns Python natives. The (optional)
    default will be returned if the environment variable does not exist.
    """
    try:
        value = os.environ[key]
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return value
    except KeyError:
        if default or not required:
            return default
        raise RuntimeError("Missing required environment variable '%s'" % key)


DATABASE_USERNAME = env('FB_DATABASE_USERNAME')
DATABASE_PASSWORD = env('FB_DATABASE_PASSWORD')
DATABASE_URL = env('FB_DATABASE_URL')

driver = GraphDatabase.driver(DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD)))

app.config['SECRET_KEY'] = env('SECRET_KEY')

docs = FlaskApiSpec(app)



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


def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'no authorization provided'}, 401
        return f(*args, **kwargs)
    return wrapped

class TestResponseSchema(Schema):
    message = fields.Str(default='Success')


class TestResponseSchema(Schema):
    api_type = fields.String(required=True, description="API type of social network API")


@app.route('/')
def SocialNetworkAPI():
        return render_template('welcome_api.html')




class PersonModel(Schema):
    type = 'object'
    properties = {
        'id': {
            'type': 'string',
        },
        'firstname': {
            'type': 'string',
        },
        'surname': {
            'type': 'string',
        },
        'email': {
            'type': 'string',
        },
        'phone_number': {
            'type': 'string',
        },
        'created_at': {
            'type': 'date',
        }
    }

def serialize_person(person):
    return {
        'id': person['id'],
        'firstname': person['firstname'],
        'surname': person['surname'],
        'email': person['email'],
        'phone_number': person['phone_number'],
        'created_at': person['created_at']
    }


class PersonsList(MethodResource, Resource):
    @swagger.doc({
        'tags': ['Persons'],
        'summary': 'Find movie by ID',
        'description': 'Returns a list of persons that subscribed',
        'parameters': [
            {
                'name': 'Authorization',
                'in': 'header',
                'type': 'string',
                'default': 'Token <token goes here>',
                'required': False
            },
        ],
        'responses': {
            '200': {
                'description': 'A Person',
                
                'schema': {
                    'type': 'array',
                    'items': PersonModel,
                },
            },
            '404': {
                'description': 'person not found'
            },
        }
    })
    def get(self):
        def get_persons(tx):
            return list(tx.run(
                '''
                MATCH (person:Person) RETURN person
                '''
            ))
        db = get_db()
        result = db.read_transaction(get_persons)
        return [serialize_person(record['person']) for record in result]



api.add_resource(PersonsList, '/persons')
docs.register(PersonsList)

if __name__ == '__main__':
    app.run(debug=True)