

from flask import Flask, g, request, send_from_directory, abort, request_started,render_template
from flask_restful import Resource, Api, reqparse
from apispec import APISpec
from marshmallow import Schema, fields

from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_restful_swagger_2 import Api, swagger, Schema




from config import env,app,api,docs,output_json
from models import PersonModel,serialize_person
import config,login,models









def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'no authorization provided'}, 401
        return f(*args, **kwargs)
    return wrapped



@app.route('/')
def SocialNetworkAPI():
        return render_template('welcome_api.html')






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