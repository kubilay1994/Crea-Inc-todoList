# from marshmallow_dataclass import dataclass


from datetime import datetime


from dataclasses import dataclass


@dataclass(frozen=True)
class TokenInfo:
    expired_at: datetime
    access_token: str
