from typing import Iterable, List, Optional

from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy import select, delete
from sqlalchemy.sql.expression import update

from core.entities.todo import Todo
from app.helpers import assign_dict_values_to_object


class TodoRepo:

    db: async_scoped_session

    def __init__(self, db: async_scoped_session):
        self.db = db

    async def get_user_todo(self, todo_id: int, user_id: int) -> Optional[Todo]:
        user: Optional[Todo] = (
            await self.db.execute(
                select(Todo).where(Todo.id == todo_id and Todo.user_id == user_id)
            )
        ).scalar()
        return user

    async def get_user_todos(self, user_id: int) -> Iterable[Todo]:
        todos: List[Todo] = (
            (await self.db.execute(select(Todo).where(Todo.user_id == user_id)))
            .scalars()
            .all()
        )
        return todos

    async def get_todos(self, todo_ids: Optional[List[int]]):

        stmt = (
            select(Todo)
            if todo_ids is None
            else select(Todo).where(Todo.id.in_(todo_ids))
        )
        todos: List[Todo] = (await self.db.execute(stmt)).scalars().all()
        return todos

    async def create_todos(self, todos: List[Todo]):
        self.db.add_all(todos)
        await self.db.commit()
        return todos

    async def create_todo(self, todo: Todo) -> Todo:
        self.db.add(todo)
        await self.db.commit()
        return todo

    async def update_user_todo(self, todo: dict) -> Optional[Todo]:
        todo_id: int = todo["id"]
        user_id: int = todo["user_id"]

        entity = await self.get_user_todo(todo_id, user_id)

        if entity is None or entity.user_id != todo["user_id"]:
            return None

        assign_dict_values_to_object(todo, entity)
        await self.db.commit()
        return entity



    async def delete_todos(self, todo_ids: List[int]):
        res = await self.db.execute(delete(Todo).where(Todo.id.in_(todo_ids)))
        await self.db.commit()
        return res.rowcount > 0

    async def delete_user_todo(self, todo_id: int, user_id: int) -> Optional[int]:
        res = await self.db.execute(
            delete(Todo).where(Todo.id == todo_id and Todo.user_id == user_id)
        )
        await self.db.commit()
        return todo_id if res.rowcount == 1 else None
