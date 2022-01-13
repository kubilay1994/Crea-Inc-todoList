from apiflask.schemas import Schema
from apiflask.fields import String, Integer,Boolean
from marshmallow.validate import Length


class RegisterSchema(Schema):
    username = String(required=True)
    password = String(required=True, validate=Length(min=6))
    is_admin = Boolean()


class UserSchema(Schema):
    username = String(required=True)
    password = String(required=True, validate=Length(min=6))

class UserOutSchema(Schema):
    id = Integer()
    username = String()
    message = String()
    

