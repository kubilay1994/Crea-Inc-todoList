from typing import List, Optional

from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

from core.entities import User


from app.helpers import assign_dict_values_to_object


class UserRepo:

    db: async_scoped_session

    def __init__(self, db: async_scoped_session):
        self.db = db

    async def get_users(self) -> List[User]:
        users_result = await self.db.execute(
            select(User).options(joinedload(User.role))
        )
        return users_result.scalars().all()

    async def get_user(self, user_name: str) -> Optional[User]:
        user: Optional[User] = (
            await self.db.execute(
                select(User)
                .where(User.username == user_name)
                .options(joinedload(User.role))
            )
        ).scalar()
        return user

    async def create_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        return user

    async def update_user(self, user: User) -> Optional[User]:
        user_id: int = user["id"]
        entity = await self.get_user(user_id)
        assign_dict_values_to_object(user, entity)
        await self.db.commit()

        return entity

    async def delete_user(self, user_id: int) -> int:
        await self.db.execute(delete(User).where(User.id == user_id))
        await self.db.commit()
        return user_id
