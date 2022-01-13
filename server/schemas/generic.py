from apiflask import Schema
from apiflask.fields import String


class GenericSchema(Schema):
    message = String(required=True)
