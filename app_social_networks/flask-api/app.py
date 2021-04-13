

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
from constants import FRIENDS_REQUEST_STATUS



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



class FriendsList(MethodResource, Resource):
    @swagger.doc({
        'tags': ['Friends'],
        'summary': 'Find the friends of a friend with id=@id',
        'description': 'Returns a list of the friends of a person that subscribed to the website',
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
    #@login_required
    def get(self):
        
        db = get_db()
        result = db.read_transaction(get_friends, g.user['id'])
        return [serialize_person(record['person']) for record in result]

def get_friends(tx,user_id):
            return list(tx.run(
                '''
                MATCH (me:Person {id: $user_id})-[my:FRIENDS_REQUEST]->(p:Person)
                WHERE me <> p
                AND my.status={accepted}
                return p
                ORDER BY created_at asc
                ''', {'user_id': user_id}
            ))

class RecommendedFriends(MethodResource, Resource):
    @swagger.doc({
        'tags': ['friends'],
        'summary': 'A list of recommended friends for the authorized user.',
        'description': 'A list of recommended friends for the authorized user.',
        'parameters': [
            {
                'name': 'Authorization',
                'in': 'header',
                'type': 'string',
                'default': 'Token <token goes here>',
                'required': True
            },
        ],
        'responses': {
            '200': {
                'description': 'A list of recommended movies for the authorized user',
                'schema': {
                    'type': 'array',
                    'items': PersonModel,
                }
            }
        }
    })
    #@login_required
    def get(self):
        db = get_db()
        list_friends= db.read_transaction(get_friends, g.user['id'])
        list_recommended_friends = []
        list_recommended_friends_corrected = []
        list_friends_id= []
        for friend in list_friends:
            list_friends_id.append(friend['id'])
        for friend in list_friends:
            recommendations = db.read_transaction(get_friends, friend['id'])
        for friend in list_recommended_friends:
            if(not(friend['id'] in list_friends_id)):
                list_recommended_friends_corrected.append(friend)
                
        return [serialize_person(record['person']) for record in list_recommended_friends_corrected]



api.add_resource(FriendsList, '/friends')
docs.register(FriendsList)


api.add_resource(RecommendedFriends, '/recommended-friends')
docs.register(RecommendedFriends)







if __name__ == '__main__':
    app.run(debug=True)