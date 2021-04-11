from flask_restful_swagger_2 import Api, swagger, Schema

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
        'date_of_birth': {
            'type': 'string',
        },
        'phone_number': {
            'type': 'string',
        },
        'password': {
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
        'date_of_birth': person['date_of_birth'],
        'phone_number': person['phone_number'],
        'password': person['password'],
        'created_at': person['created_at']
    }



class PageModel(Schema):
    type = 'object'
    properties = {
        'id': {
            'type': 'string',
        },
        'name_page': {
            'type': 'string',
        },
        'about': {
            'type': 'text',
        },
        'url_website': {
            'type': 'string',
        },
        'type': {
            'type': 'string',
        },
        'created_at': {
            'type': 'datetime',
        }
    }

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
    type = 'object'
    properties = {
        'id': {
            'type': 'string',
        },
        'group_name': {
            'type': 'string',
        },
        'visibility': {
            'type': 'string',
        },
        'created_at': {
            'type': 'date',
        }
    }

def serialize_group(group):
    return {
        'id': group['id'],
        'group_name': group['group_name'],
        'visibility': group['visibility'],
        'created_at': group['created_at']
    }


class MediaModel(Schema):
    type = 'object'
    properties = {
        'id': {
            'type': 'string',
        },
        'local_path': {
            'type': 'string',
        },
        'category': {
            'type': 'string',
        },
        'created_at': {
            'type': 'date',
        }
    }

def serialize_media(model):
    return {
        'id': model['id'],
        'local_path': model['local_path'],
        'category': model['category'],
        'created_at': model['created_at']
    }

class MessageModel(Schema):
    type = 'object'
    properties = {
        'id': {
            'type': 'string',
        },
        'html_content': {
            'type': 'text',
        },
        'created_at': {
            'type': 'date',
        }
    }

def serialize_message(model):
    return {
        'id': model['id'],
        'html_content': model['html_content'],
        'created_at': model['created_at']
    }


class CommentModel(Schema):
    type = 'object'
    properties = {
        'id': {
            'type': 'string',
        },
        'html_content': {
            'type': 'text',
        },
        'created_at': {
            'type': 'date',
        }
    }

def serialize_comment(model):
    return {
        'id': model['id'],
        'html_content': model['html_content'],
        'created_at': model['created_at']
    }


class FriendRequestModel(Schema):
    type = 'object'
    properties = {
        'id': {
            'type': 'string',
        },
        'status': {
            'type': 'string',
        },
        'created_at': {
            'type': 'datetime',
        }
    }

def serialize_friendrequest(model):
    return {
        'id': model['id'],
        'status': model['status'],
        'created_at': model['created_at']
    }

class PostModel(Schema):
    type = 'object'
    properties = {
        'id': {
            'type': 'string',
        },
        'html_content': {
            'type': 'text',
        },
        'type': {
            'type': 'string',
        },
        'created_at': {
            'type': 'date',
        }
    }

def serialize_post(model):
    return {
        'id': model['id'],
        'html_content': model['html_content'],
        'type': model['type'],
        'created_at': model['created_at']
    }
