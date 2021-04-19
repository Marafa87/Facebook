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
from flask_jwt_extended import JWTManager
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
#from flask_restful_swagger_2 import Api, swagger, Schema

from functools import wraps


from login import set_user
from config import env,app,api,docs,output_json,db_mg
from models2 import PersonModelMG,PageListMG,PostsListMG,PostModelMG,ProfilModelMG,RegisterPersonModelMG,FriendsListModelMG
import config,login,models
from constants import FRIENDS_REQUEST_STATUS


import logging




#create a logger
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

def hash_password_mg(username, password):
    if sys.version[0] == 2:
        s = '{}:{}'.format(username, password)
    else:
        s = '{}:{}'.format(username, password).encode('utf-8')
    return hashlib.sha256(s).hexdigest()



def login_required_mg(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'no authorization provided'}, 401
        return f(*args, **kwargs)
    return wrapped




class FriendsListMG(MethodResource, Resource):
    @doc(description='List of friends', tags=['MONGO Person'])
    @marshal_with(FriendsListModelMG)  # marshalling
    #@login_required_mg
    def get(self,id):
      
        result = list(db_mg.Person.aggregate([
                {
                "$addFields": {"_id_person": {'$toString':'$_id'}}
                },
                {
                    "$match":{   
                        "_id_person":id_person
                        },
                } ,
                {
                    '$lookup': {
                        'from': 'Person', 
                        'localField': '_id_person', 
                        'foreignField': 'id_sender',
                        'as': 'friends2',
                        'as': 'friends',
                    }
                }, 
                {
                    '$lookup': {
                        'from': 'Person', 
                        'localField': 'id_sender', 
                        'foreignField': '_id',
                        'as': 'friends2',
                    }
                }, 
                {
                    '$unwind': {
                        'path': '$friends', 
                        'preserveNullAndEmptyArrays': True
                    }
                }, 
                {
                    '$unwind': {
                        'path': '$friends2', 
                        'preserveNullAndEmptyArrays': True
                    }
                } ]) )        
        return {'friends':result["friends"]},200



class PostsFromPageMG(MethodResource, Resource):
    @doc(description='List of Posts from page', tags=['MONGO Post'])
    @marshal_with(PostsListMG)  # marshalling
    #@login_required_mg
    def get(self,id):
      
        result = list(db_mg.Pages.aggregate([
                {
                "$addFields": {"_id_page": {'$toString':'$_id'}}
                },
                {
                    "$match":{   
                        "_id_page":id
                        },
                }, 
                {
                    '$lookup': {
                        'from': 'Posts', 
                        'localField': 'id_page_owner', 
                        'foreignField': 'Pages._id', 
                        'as': 'posts',
                    }
                }, 
                {
                    '$unwind': {
                        'path': '$posts', 
                        'preserveNullAndEmptyArrays': True
                    }
                } 
                ,{
                    "$limit":20
                }
              
                ]
                ) )        
        for record in result:
            app.logger.error("POST")
        return {'posts': result['posts']},200

class PostsFromFriendsAndPageMG(MethodResource, Resource):
    @doc(description='List of Posts from page', tags=['MONGO Post'])
    @marshal_with(PostsListMG)  # marshalling
    #@login_required_mg
    def get(self,id):
      
        result = list(db_mg.Pages.aggregate([
                {
                "$addFields": {"_id_page": {'$toString':'$_id'}}
                },
                {
                    "$match":{   
                        "_id_page":id
                        },
                }, 
                {
                    '$lookup': {
                        'from': 'Posts', 
                        'localField': 'id_owner_of_wall_to_display', 
                        'foreignField': 'Pages._id_page', 
                        'as': 'posts',
                    }
                }, 
                {
                    '$unwind': {
                        'path': '$posts', 
                        'preserveNullAndEmptyArrays': True
                    }
                } 
                ,{
                    "$limit":20
                }
              
                ]
                ) )        
        for record in result:
            app.logger.error("POST")
        return {'posts': result['posts']},200


api.add_resource(FriendsListMG, '/mongodb/friends/<string:id>')
api.add_resource(PostsFromPageMG, '/mongodb/page-posts/<string:id>')
api.add_resource(PostsFromFriendsAndPageMG, '/mongodb/page-friends-posts/<string:id>')


#api.add_resource(RecommendedFriends, '/mongodb/recommended-friends/<string:id>')
#api.add_resource(Messages, '/mongodb/messages/<string:id>')
#api.add_resource(Photos, '/mongodb/photos/<string:id>')

docs.register(FriendsListMG)
docs.register(PostsFromPageMG)
docs.register(PostsFromFriendsAndPageMG)
