from typing import Optional
from core.entities import User
import bcrypt

from core.models import TokenInfo
from app.services.auth.TokenService import TokenService
from app.repos.auth.UserRepo import UserRepo


class UserService:
    repo: UserRepo
    token_service: TokenService

    def __init__(self, repo: UserRepo, token_service: TokenService):
        self.repo = repo
        self.token_service = token_service

    async def get_users(self):
        return await self.repo.get_users()

    async def login(self, user: User) -> Optional[TokenInfo]:
        entity = await self.repo.get_user(user.username)

        if entity and bcrypt.checkpw(user.password.encode("utf-8"), entity.password):
            return self.token_service.create_token(entity)

    async def register(self, user: User) -> User:

        user.password = bcrypt.hashpw(str.encode(user.password), bcrypt.gensalt())
        return await self.repo.create_user(user)
