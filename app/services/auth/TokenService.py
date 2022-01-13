from core.entities import User
from core.models import TokenInfo

import jwt
import os

from datetime import datetime, timedelta


secret = os.getenv("JWT_SECRET", "asaghdffashadfgdsafdsfas")


class TokenService:
    def create_token(self, user: User) -> TokenInfo:
        token = jwt.encode(
            {
                "exp": datetime.utcnow() + timedelta(minutes=25),
                "user_id": user.id,
                "role": user.role.name,
            },
            key=secret,
        )
        return TokenInfo(
            expired_at=datetime.utcnow() + timedelta(minutes=25), access_token=token
        )
