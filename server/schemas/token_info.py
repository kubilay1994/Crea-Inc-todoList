from marshmallow_dataclass import class_schema

from core.models.auth.token_info import TokenInfo


TokenInfoSchema = class_schema(TokenInfo)
