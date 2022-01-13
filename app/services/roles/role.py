from sqlalchemy.sql.sqltypes import Enum
from app.repos import RoleRepo

from cachetools import cached, TTLCache

cache = TTLCache(maxsize=1, ttl=60 * 60 * 24)



class RoleService:
    repo: RoleRepo

    def __init__(self, repo: RoleRepo):
        self.repo = repo

    @cached(cache=cache)
    async def get_roles(self):
        return await self.repo.get_roles()
