from typing import List

from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import select

from core.entities import Role


class RoleRepo:

    db: async_scoped_session

    def __init__(self, db: async_scoped_session):
        self.db = db

    async def get_roles(self) -> List[Role]:
        roles = (await self.db.execute(select(Role))).scalars().all()
        return roles
