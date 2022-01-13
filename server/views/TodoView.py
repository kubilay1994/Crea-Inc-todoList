from typing import Optional
from werkzeug.exceptions import NotFound
from core.entities.todo import Todo

from apiflask import input


from flask.views import MethodView


from main import dep_container
from lagom.decorators import magic_bind_to_container
from apiflask.decorators import auth_required, doc, output
from server.schemas.todo import TodoOutSchema, TodoSchema

from app.services.todos.TodoService import TodoService

from server.security import user_auth


class TodoView(MethodView):

    decorators = [auth_required(user_auth)]

    todoService: TodoService

    @magic_bind_to_container(container=dep_container)
    def __init__(self, todoService: TodoService) -> None:
        self.todoService = todoService

    @output(TodoOutSchema)
    @doc(
        summary="Gets a todo",
        description=" Gets todo item with given id if todo is owned by user",
    )
    async def get(self, user_id: int, todo_id: int):

        print(todo_id, user_id)
        res = await self.todoService.get_user_todo(todo_id, user_id)
        if res is None:
            raise NotFound
        return res

    @input(TodoSchema)
    @output(TodoOutSchema, status_code=201)
    @doc(
        summary="Creates a todo",
        description=" Creates todo item for the user",
    )
    async def post(self, user_id: int, todo: dict):

        todo["user_id"] = user_id
        created = await self.todoService.create_todo(Todo(**todo))
        return created

    @input(TodoSchema)
    @output(TodoOutSchema, status_code=200)
    @doc(
        summary="Updates a todo",
        description=" Updates todo item if owned by the user",
    )
    async def put(self, user_id: int, todo_id: int, todo: dict):

        todo["id"] = todo_id
        todo["user_id"] = user_id
        print(todo)
        res = await self.todoService.update_user_todo(todo)
        if res is None:
            raise NotFound
        return res

    async def delete(self, user_id: int, todo_id: int):
        """Deletes a todo


        Deletes todo item beloging the user
        """
        todo_id = await self.todoService.delete_user_todo(todo_id, user_id=user_id)
        if todo_id is None:
            return {"message": "todo for user does not exist"}, 404
        return {"message": "successfully deleted", "todo_id": todo_id}
