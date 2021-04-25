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
from datetime import timedelta
from flask import Flask, g, request, send_from_directory, abort, request_started,render_template
from flask_restful import Resource, Api, reqparse
from apispec import APISpec
from marshmallow import Schema, fields
from flask_jwt_extended import JWTManager
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
#from flask_restful_swagger_2 import Api, swagger, Schema
from flask_jwt_extended import create_access_token
from functools import wraps


from login import get_db,close_db,set_user
from config import env,app,api,docs,output_json
from models import serialize_post,serialize_media,serialize_message,PersonModel,MediaListModel,MessageListModel,PostModel,serialize_person,RegisterPersonModel,FriendsListModel,PostsListModel
import config,login,models
from constants import FRIENDS_REQUEST_STATUS

import app2
import logging

#create a logger
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

def hash_password(username, password):
    if sys.version[0] == 2:
        s = '{}:{}'.format(username, password)
    else:
        s = '{}:{}'.format(username, password).encode('utf-8')
    return hashlib.sha256(s).hexdigest()



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




def get_friends(tx,user_id):
            accepted='ACCEPTED'
            return list(tx.run(
                '''
                MATCH (me:Person {id: $user_id})-[my:FRIEND_REQUEST]-(person:Person)
                WHERE me <> person
                AND my.status= $accepted
                return person
                ORDER BY my.created_at ASC
                ''', {'user_id': user_id,'accepted':accepted}
            ))





class FriendsList(MethodResource, Resource):
    @doc(description='List of friends', tags=['NEO4J Person'])
    @marshal_with(FriendsListModel)  # marshalling
    #@login_required
    def get(self,id):
        
        db = get_db()
        result = db.read_transaction(get_friends, id)
        for record in result:
            app.logger.error(serialize_person(record['person']))
        return {'friends':[serialize_person(record['person']) for record in result]}



class RecommendedFriends(MethodResource, Resource):
    @doc(description='List of recommended friends', tags=['NEO4J Person'])
    @marshal_with(FriendsListModel)  # marshalling
    #@login_required
    def get(self,id):
        db = get_db()
        list_friends= db.read_transaction(get_friends, id)
        list_recommended_friends = []
        list_recommended_friends_corrected = []
        list_friends_id= []
        for record in list_friends:
            list_friends_id.append(record['person'].get('id'))
        for friend in list_friends:
            recommendations = db.read_transaction(get_friends, friend['person'].get('id'))
            list_recommended_friends.extend(recommendations)
        list_friends_id.append(id)
        for friend in list_recommended_friends:
            
            if(not(friend['person'].get('id') in list_friends_id)):
                if(not(friend in list_recommended_friends_corrected)):
                    list_recommended_friends_corrected.append(friend)
        app.logger.error(list_recommended_friends_corrected)      
        return {'friends':[serialize_person(record['person']) for record in list_recommended_friends_corrected]}

class PostsFromPage(MethodResource, Resource):
    @doc(description='List of Posts from page', tags=['NEO4J Post'])
    @marshal_with(PostsListModel)  # marshalling
    #@login_required_mg
    def get(self,id):
        db = get_db()
        def get_posts(tx,page_id):
            return list(tx.run(
                '''
                MATCH (page:Page {id: $page_id})--(post:Post)
                return post
                ORDER BY post.created_at DESC
                LIMIT 20
                ''', {'page_id': page_id}
            ))
        result = db.read_transaction(get_posts, id)
        for record in result:
            app.logger.error("POST")
        return {'posts':[serialize_post(record['post']) for record in result]},200

class PostsFromFriendsAndPage(MethodResource, Resource):
    @doc(description='List of Posts from page followed and friends', tags=['NEO4J Post'])
    @marshal_with(PostsListModel)  # marshalling
    #@login_required_mg
    def get(self,id):
      
        db = get_db()
        def get_posts(tx,person_id):
            return list(tx.run(
                '''
                MATCH (person:Person {id: $person_id})-[*..2]-(post:Post)
                return post
                ORDER BY post.created_at DESC
                LIMIT 20
                ''', {'person_id': person_id}
            ))
        result = db.read_transaction(get_posts, id)
        app.logger.error(result)
        return {'posts':[serialize_post(record['post']) for record in result]},200


class Messages(MethodResource, Resource):
    @doc(description='List of Message from friends of a person', tags=['NEO4J Message'])
    @marshal_with(MessageListModel)  # marshalling
    #@login_required_mg
    def get(self,id):
        db = get_db()
        def get_messages(tx,person_id):
            return list(tx.run(
                '''
                MATCH (person:Person {id: $person_id})--(message:Message)
                return message 
                ORDER BY message.created_at DESC
                LIMIT 20
                ''', {'person_id': person_id}
            ))
        result = db.read_transaction(get_messages, id)
        for record in result:
            app.logger.error("MESSAGE")
        return {'messages':[serialize_message(record['message']) for record in result]},200

class Photos(MethodResource, Resource):
    @doc(description='List of Photos of a person', tags=['NEO4J Photo'])
    @marshal_with(MediaListModel)  # marshalling
    #@login_required_mg
    def get(self,id):
        db = get_db()
        def get_photos(tx,person_id):
            return list(tx.run(
                '''
                MATCH (person:Person {id: $person_id})--(media:Media)
                WHERE media.category = 'PHOTO'
                return media
                ORDER BY media.created_at desc
                LIMIT 20
                ''', {'person_id': person_id}
            ))
        result = db.read_transaction(get_photos, id)
        for record in result:
            app.logger.error("record")
        return {'medias':[serialize_media(record['media']) for record in result]},200

class Register(MethodResource, Resource):
    @doc(description='Register a new person', tags=['NEO4J Person'],authorization=False)
    @use_kwargs(RegisterPersonModel, location=('json'))
    @marshal_with(PersonModel)  # marshalling
    def post(self, **kwargs):
        data = request.get_json()
        surname = kwargs.get('surname')
        firstname = kwargs.get('firstname')
        email = kwargs.get('email')
        date_of_birth = kwargs.get('date_of_birth')
        phone_number = kwargs.get('phone_number')
        password = kwargs.get('password')
        if not email:
            return {'email': 'This field is required.'}, 400
        if not surname:
            return {'surname': 'This field is required.'}, 400
        if not firstname:
            return {'firstname': 'This field is required.'}, 400
        if not date_of_birth:
            return {'date_of_birth': 'This field is required.'}, 400
        if not password:
            return {'password': 'This field is required.'}, 400

        def get_user_by_email(tx, username):
            return tx.run(
                '''
                MATCH (person:Person {email: $username}) RETURN person
                ''', {'username': username}
            ).single()

        db = get_db()
        result = db.read_transaction(get_user_by_email, email)
        if result and result.get('person'):
            return {'username': 'username already in use'}, 400
        now = (datetime.now()).strftime('%Y/%m/%d')
        def create_user(tx, email,surname,firstname,date_of_birth,now,phone_number, password):
            return tx.run(
                '''
                CREATE (person:Person {id: $id,created_at: $now, email: $email, surname: $surname, firstname: $firstname, phone_number: $phone_number, date_of_birth: $date_of_birth, password: $password, api_key: $api_key}) RETURN person
                ''',
                {
                    'id': str(uuid.uuid4()),
                    'email': email,
                    'surname': surname,
                    'firstname': firstname,
                    'date_of_birth': date_of_birth,
                    'phone_number': phone_number,
                   # 'password': hash_password(email, password),
                   'password': password,
                    'now':now,
                    'api_key': binascii.hexlify(os.urandom(20)).decode()
                }
            ).single()

        results = db.write_transaction(create_user, email,surname,firstname,date_of_birth,now,phone_number, password)
        user = results['person']
        return user, 201


class StandardResponseSchema(Schema):
    message = fields.Str(default='Success')

class TokenResponseSchema(Schema):
    token = fields.Str(default='Success')



class LoginPersonSchema(Schema) : 
    username = fields.String(required=True)
    password = fields.String(required=True)

class Login(MethodResource, Resource):
    @doc(description='Login', tags=['NEO4J Person'])
    @use_kwargs(LoginPersonSchema, location=('json'))
    @marshal_with(TokenResponseSchema)  # marshalling
    def post(self, **kwargs):
        data = request.get_json()
        app.logger.error('LOGIN DEBUG')
        email = kwargs.get('username')
        password = kwargs.get('password')
        logger.debug('LOGIN EMAIL: '+email)
        if not email:
            return {'username': 'This field is required.'}, 400
        if not password:
            return {'password': 'This field is required.'}, 400
        

        def get_user_by_email(tx, email):
            return tx.run(
                '''
                MATCH (person:Person {email: $email}) RETURN person
                ''', {'email': email}
            ).single()

        def update_token_user(tx,email,api_key):
            return tx.run(
                '''
                MATCH (person:Person {email: $email}) set person.api_key=$api_key RETURN person
                ''', {'email': email,'api_key':api_key}
            ).single()

        db = get_db()
        result = db.read_transaction(get_user_by_email, email)
        
        
        if not result:
            return {'username': 'No user found with this username.'}, 400
        
        try:
            user = result.get('person')
            
        except KeyError:
            return {'username': 'unknown username'}, 400

        expected_password = hash_password(user['email'], password)
        expected_password = user['password']
        if user['password'] != expected_password:
            return {'password': 'invalid password'}, 400
        else:
            expires = timedelta(days=7)
            api_key = create_access_token(identity=str(user.id), expires_delta=expires)
            result= db.write_transaction(update_token_user,email,api_key)
            user = result['person']
        return {'token': user['api_key'] },200


class UserMe(MethodResource, Resource):
    @doc(description='Me', tags=['NEO4J Person'])
    @marshal_with(PersonModel)  # marshalling
    @login_required
    def get(self):
        return serialize_user(g.user)

api.add_resource(FriendsList, '/neo4j/friends/<string:id>')
api.add_resource(RecommendedFriends, '/neo4j/recommended-friends/<string:id>')
api.add_resource(PostsFromPage, '/neo4j/page-posts/<string:id>')
api.add_resource(PostsFromFriendsAndPage, '/neo4j/page-friends-posts/<string:id>')

api.add_resource(Messages, '/neo4j/messages/<string:id>')
api.add_resource(Photos, '/neo4j/photos/<string:id>')

api.add_resource(Register, '/neo4j/register')
api.add_resource(Login, '/neo4j/login')
api.add_resource(UserMe, '/neo4j/users/me')

docs.register(FriendsList)
docs.register(RecommendedFriends)
docs.register(PostsFromPage)
docs.register(PostsFromFriendsAndPage)

docs.register(Messages)
docs.register(Photos)

docs.register(Register)
docs.register(Login)
docs.register(UserMe)





if __name__ == '__main__':
    app.run(debug=True)