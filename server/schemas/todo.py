


from apiflask import Schema
from apiflask.fields import String, Integer,List
from apiflask.validators import Length,URL

from marshmallow import validates
from marshmallow.exceptions import ValidationError


class TodoSchema(Schema):
    name = String(required=True)
    description = String(required=True, validate=Length(min=30))
    video_link = String(validate=URL(relative=False))
    image_link = String(validate=URL(relative=False))


class TodoOutSchema(TodoSchema):
    id = Integer()


class TodoIDsSchema(Schema):
    todo_ids = List(Integer)

    @validates('todo_ids')
    def no_duplicate_ids(self, value):
        if len(value) != len(set(value)):
            raise ValidationError('todo ids must not contain duplicate elements')

