
from marshmallow import Schema, fields




class PersonModel(Schema):
    id = fields.String(required=True)
    firstname = fields.String(required=True)
    surname = fields.String(required=True)
    email = fields.String(required=True)
    date_of_birth = fields.String(required=True)
    phone_number = fields.String(required=True)
    password = fields.String(required=True)
    created_at = fields.String(required=True)
    api_key = fields.String(required=False)

class FriendsListModel(Schema):
    friends= fields.List(fields.Nested(PersonModel))

class RegisterPersonModel(Schema):
    firstname = fields.String(required=True)
    surname = fields.String(required=True)
    email = fields.String(required=True)
    date_of_birth = fields.String(required=True)
    phone_number = fields.String(required=True)
    password = fields.String(required=True)

def serialize_person(person):
    return {
        'id': person['id'],
        'firstname': person['firstname'],
        'surname': person['surname'],
        'email': person['email'],
        'date_of_birth': person['date_of_birth'],
        'phone_number': person['phone_number'],
        'password': person['password'],
        'created_at': person['created_at'],
        'api_key': person['api_key']
    }



class PageModel(Schema):
    id = fields.String(required=True)
    name_page = fields.String(required=True)
    about = fields.String(required=True)
    url_website = fields.String(required=True)
    type = fields.String(required=True)
    created_at = fields.Date(required=True)

def serialize_page(page):
    return {
        'id': page['id'],
        'name_page': page['name_page'],
        'about': page['about'],
        'url_website': page['url_website'],
        'type': page['type'],
        'created_at': page['created_at']
    }


class GroupModel(Schema):
    id = fields.String(required=True)
    group_name = fields.String(required=True)
    visibility = fields.String(required=True)
    created_at = fields.Date(required=True)

def serialize_group(group):
    return {
        'id': group['id'],
        'group_name': group['group_name'],
        'visibility': group['visibility'],
        'created_at': group['created_at']
    }


class MediaModel(Schema):
    id = fields.String(required=True)
    type = fields.String(required=True)
    local_path = fields.String(required=True)
    category = fields.String(required=True)
    created_at = fields.String(required=True)

class MediaListModel(Schema):
    medias= fields.List(fields.Nested(MediaModel))

def serialize_media(model):
    return {
        'id': model['id'],
        'local_path': model['local_path'],
        'category': model['category'],
        'created_at': model['created_at']
    }

class MessageModel(Schema):
    id = fields.String(required=True)
    type = fields.String(required=True)
    html_content = fields.String(required=True)
    created_at = fields.String(required=True)

class MessageListModel(Schema):
    messages= fields.List(fields.Nested(MessageModel))

def serialize_message(model):
    return {
        'id': model['id'],
        'html_content': model['html_content'],
        'created_at': model['created_at']
    }


class CommentModel(Schema):
    id = fields.String(required=True)
    html_content = fields.String(required=True)
    created_at = fields.Date(required=True)

def serialize_comment(model):
    return {
        'id': model['id'],
        'html_content': model['html_content'],
        'created_at': model['created_at']
    }


class FriendRequestModel(Schema):
    id = fields.String(required=True)
    status = fields.String(required=True)
    created_at = fields.Date(required=True)
    

def serialize_friendrequest(model):
    return {
        'id': model['id'],
        'status': model['status'],
        'created_at': model['created_at']
    }

class PostModel(Schema):
    id = fields.String(required=True)
    html_content = fields.String(required=True)
    type=fields.String(required=True)
    created_at = fields.String(required=True)

class PostsListModel(Schema):
    posts= fields.List(fields.Nested(PostModel))

def serialize_post(model):
    return {
        'id': model['id'],
        'html_content': model['html_content'],
        'type': model['type'],
        'created_at': model['created_at']
    }
