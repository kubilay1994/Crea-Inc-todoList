import os
from apiflask.security import HTTPTokenAuth
import jwt
from flask import request


user_auth = HTTPTokenAuth(description="Simple Bearer token with user information")


@user_auth.get_user_roles
async def get_roles(user):
    return user["role"]


@user_auth.verify_token
def verify_token(token: str):

    user_id = request.view_args.get("user_id") if request.view_args else None
    try:
        secret = os.getenv("JWT_SECRET")
        verified_token = jwt.decode(token, secret, algorithms=["HS256"])
        return (
            {
                "user_id": verified_token["user_id"],
                "role": verified_token["role"],
            }
            if user_id is None or user_id == verified_token["user_id"]
            else False
        )

    except Exception:
        return False
