
from marshmallow import Schema, fields



class ProfilModelMG(Schema):
    Name = fields.String(required=True)
    Surname = fields.String(required=True)


class PersonModelMG(Schema):
    _id = fields.String(required=True)
    profil_info = fields.Nested(ProfilModelMG)
    Email = fields.String(required=True)
    date_of_birth = fields.String(required=True)
    Phonenumber = fields.String(required=True)
    Password = fields.String(required=True)
    created_at = fields.String(required=True)

class FriendsListModelMG(Schema):
    friends= fields.List(fields.Nested(PersonModelMG))

class PostOwnerModel(Schema):
    id_page_owner = fields.String()
    id_person_owner = fields.String()


class PostModelMG(Schema):
    _id = fields.String(required=True)
    html_content = fields.String(required=True)
    owner = fields.Nested(PostOwnerModel)
    id_owner_of_wall_to_display: fields.String(required=True)
    id_comments = fields.List(fields.String())
    _type = fields.String(required=True)
    created_at = fields.Date(required=True)


class PostsListMG(Schema):
    friends= fields.List(fields.Nested(PostModelMG))

class RegisterPersonModelMG(Schema):
    firstname = fields.String(required=True)
    surname = fields.String(required=True)
    email = fields.String(required=True)
    date_of_birth = fields.DateTime(required=True)
    phone_number = fields.String(required=True)
    password = fields.String(required=True)


class PageModelMG(Schema):
    _id = fields.String(required=True)
    name_page = fields.String(required=True)
    about = fields.String(required=True)
    url_website = fields.String(required=True)
    type = fields.String(required=True)
    created_at = fields.Date(required=True)


class PageListMG(Schema):
    pages= fields.List(fields.Nested(PageModelMG))

class GroupModel(Schema):
    _id = fields.String(required=True)
    group_name = fields.String(required=True)
    visibility = fields.String(required=True)
    created_at = fields.Date(required=True)


class MediaModel(Schema):
    _id = fields.String(required=True)
    type = fields.String(required=True)
    local_path = fields.String(required=True)
    category = fields.String(required=True)
    created_at = fields.Date(required=True)


class MessageModel(Schema):
    _id = fields.String(required=True)
    type = fields.String(required=True)
    html_content = fields.String(required=True)
    created_at = fields.Date(required=True)


class CommentModel(Schema):
    _id = fields.String(required=True)
    html_content = fields.String(required=True)
    created_at = fields.DateTime(required=True)


class FriendRequestModel(Schema):
    _id = fields.String(required=True)
    status = fields.String(required=True)
    created_at = fields.Date(required=True)


