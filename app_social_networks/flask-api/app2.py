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
from models2 import MessagesListModelMG,MessageModelMG,MediasListModelMG,MediaModelMG,PersonModelMG,PageListMG,PostsListMG,PostModelMG,ProfilModelMG,RegisterPersonModelMG,FriendsListModelMG
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




def get_friends_of_person2(id):
    result = list(db_mg.Persons.aggregate([ 
                { '$unwind': '$friend_requests' },
                {
                "$addFields": {"_id_person": {'$toString':'$_id'},
                                "id_sender_object":{'$toObjectId':'$friend_requests.sender_id'}}
                },
                
                {
                
                '$match': {
                                '_id_person': id,
                                "friend_requests.status": 'ACCEPTED',
                  
                    }
                  
                },
        
                {'$lookup': {
                    'from': 'Persons', 
                    'localField': 'id_sender_object', 
                    'foreignField': '_id', 
                    'as': 'friends_accepted'
                }
                }

                
        
     
        ]) )
    friends_requested = list(db_mg.Persons.aggregate([ 
                { '$unwind': '$friend_requests' },
            
                
                {
                
                '$match': {
                    "friend_requests.sender_id": id,
                                "friend_requests.status": 'ACCEPTED'
                  
                    }
                  
                }
     
        ]) )
    #app.logger.error(id) 
    
    friends = []
    friends_accepted = []
       
    if(len(result)>0):
        for res in result:
            friends_accepted = res.get('friends_accepted')
            for friend in friends_accepted:
                if (not(friend in friends) and (str(friend.get('_id'))!=id)):
                    friends.append(friend)
    #app.logger.error('friends_accepted')
    #app.logger.error(friends_accepted)
    #app.logger.error('friends_requested')
    #app.logger.error(friends_requested)
    for friend in friends_requested:
                if (not(friend in friends) and (str(friend.get('_id'))!=id)):
                    friends.append(friend)
    return friends



class FriendsListMG(MethodResource, Resource):
    @doc(description='List of friends', tags=['MONGO Person'])
    @marshal_with(FriendsListModelMG)  # marshalling
    #@login_required_mg
    def get(self,id):
      
        friends = get_friends_of_person2(id)      

        
        
        #app.logger.error(friends) 
        return {'friends':friends},200



class PostsFromPageMG(MethodResource, Resource):
    @doc(description='List of Posts from page', tags=['MONGO Post'])
    @marshal_with(PostsListMG)  # marshalling
    #@login_required_mg
    def get(self,id):
        posts = []
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
                        'localField': '_id_page', 
                        'foreignField': 'owner.id_page_owner', 
                        'as': 'posts',
                    }
                }, 
                { "$sort": { "created_at": -1 } },
                {
                    "$limit":20
                }
              , 
                ]) )   
        if(len(result)>0):
            posts = result[0].get('posts')
        return {'posts': posts},200


class PostsFromFriendsAndPageMG(MethodResource, Resource):
    @doc(description='List of Posts from page', tags=['MONGO Post'])
    @marshal_with(PostsListMG)  # marshalling
    #@login_required_mg
    def get(self,id):
      
        friends = get_friends_of_person2(id) 
        posts_friends = []
        for friend in friends:
            id_friend = str(friend.get('_id'))
            app.logger.error(id_friend) 
            posts_friend = list(db_mg.Posts.aggregate([
                { '$unwind': '$owner' },
                {
                    "$match":{   
                        "owner.id_person_owner":id_friend
                        },
                }, 
                { "$sort": { "created_at": -1 } },
                {
                    "$limit":20
                }
              
                ]
                ) )  
             
            if(len(posts_friend)>0):
                posts_friends.extend(posts_friend)

        app.logger.error(posts_friends)  
       
        return {'posts': posts_friends},200


class RecommendedFriendsMG(MethodResource, Resource):
    @doc(description='List of recommended friends', tags=['MONGO Person'])
    @marshal_with(FriendsListModelMG)  # marshalling
    #@login_required
    def get(self,id):
        list_friends = get_friends_of_person2(id)
        list_recommended_friends = []
        list_recommended_friends_corrected = []
        list_friends_id = []
        list_friends_id.append(str(id))
        
        for friend in list_friends:
            list_friends_id.append(str(friend.get('_id')))
            recommendations = get_friends_of_person2( str(friend.get('_id')))
            list_recommended_friends.extend(recommendations)
        
        for friend in list_recommended_friends:
            if(not(str(friend.get('_id')) in list_friends_id)):
                list_friends_id.append(str(friend.get('_id')))
                list_recommended_friends_corrected.append(friend)
          
        return {'friends':list_recommended_friends_corrected}





class PhotosMG(MethodResource, Resource):
    @doc(description='List of Photos from a person', tags=['MONGODB Photo'])
    @marshal_with(MediasListModelMG)  # marshalling
    #@login_required_mg
    def get(self,id):
        photos_person = list(db_mg.Medias.aggregate([
        
                {
                
                '$match': {
                    'category': 'PHOTO',
                    'owner.id_person_owner': id,
                    }
                },
                { "$sort": { "created_at": -1 } },
                {
                    "$limit":20
                }
              
                ]
                ) )  
        
        return {'medias':photos_person},200




api.add_resource(FriendsListMG, '/mongodb/friends/<string:id>')
api.add_resource(PostsFromPageMG, '/mongodb/page-posts/<string:id>')
api.add_resource(PostsFromFriendsAndPageMG, '/mongodb/page-friends-posts/<string:id>')


api.add_resource(RecommendedFriendsMG, '/mongodb/recommended-friends/<string:id>')
#api.add_resource(Messages, '/mongodb/messages/<string:id>')
api.add_resource(PhotosMG, '/mongodb/photos/<string:id>')

docs.register(FriendsListMG)
docs.register(PostsFromPageMG)
docs.register(PostsFromFriendsAndPageMG)
docs.register(RecommendedFriendsMG)
docs.register(PhotosMG)
