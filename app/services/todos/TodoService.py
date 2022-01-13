from typing import Iterable, List, Optional
from core.entities.todo import Todo
from app.repos.todos.TodoRepo import TodoRepo


class TodoService:
    repo: TodoRepo

    def __init__(self, repo: TodoRepo):
        self.repo = repo

    async def get_user_todo(self, todo_id: int, user_id: int) -> Optional[Todo]:
        return await self.repo.get_user_todo(todo_id, user_id)

    async def get_todos(self, todo_ids: Optional[List[int]]):
        return await self.repo.get_todos(todo_ids)

    async def get_user_todos(self, user_id: int) -> Iterable[Todo]:
        return await self.repo.get_user_todos(user_id)

    async def create_todo(self, todo: Todo) -> Todo:
        return await self.repo.create_todo(todo)

    async def create_todos(self, todos: List[Todo]):
        return await self.repo.create_todos(todos)

    async def update_user_todo(self, todo: dict) -> Todo:
        return await self.repo.update_user_todo(todo)

    async def update_todos(self, todo_ids: List[int], updates: dict):
        return await self.repo.update_todos(todo_ids, updates)

    async def delete_user_todo(self, todo_id: int, user_id: int):
        return await self.repo.delete_user_todo(todo_id, user_id)

    async def delete_todos(self, todo_ids: List[int]):
        return await self.repo.delete_todos(todo_ids)

