from typing import List
from apiflask.blueprint import APIBlueprint
from werkzeug.exceptions import NotFound
from core.entities.todo import Todo

from apiflask import input


from flask.views import MethodView


from main import dep_container
from lagom.decorators import magic_bind_to_container
from apiflask.decorators import auth_required, doc, output
from server.schemas.generic import GenericSchema
from server.schemas.todo import TodoIDsSchema, TodoOutSchema, TodoSchema

from app.services.todos.TodoService import TodoService

from server.security import user_auth


admin = APIBlueprint("admin", __name__)


@admin.route("todos")
class AdminTodoView(MethodView):

    decorators = [auth_required(user_auth, role="admin")]

    todoService: TodoService

    @magic_bind_to_container(container=dep_container)
    def __init__(self, todoService: TodoService) -> None:
        self.todoService = todoService

    @input(TodoIDsSchema, location="query")
    @output(TodoOutSchema(many=True))
    @doc(
        summary="Gets list of todos",
        description=" Gets todo items with given ids",
    )
    async def get(self, info: dict):

        res = await self.todoService.get_todos(info.pop("todo_ids", None))
        if res is None or len(res) == 0:
            raise NotFound
        return res

    @input(TodoSchema(many=True))
    @output(TodoOutSchema(many=True), status_code=201)
    @doc(
        summary="Creates todos",
        description=" Creates todo items int batches ",
    )
    async def post(self, todos: List[dict]):

        user = user_auth.current_user

        todo_items = [Todo(user_id=user["user_id"], **todo) for todo in todos]
        created_items = await self.todoService.create_todos(todo_items)
        return created_items

    @doc(
        summary="Deletes todo items",
        description=" Deletes todo items with given ids",
    )
    @input(TodoIDsSchema, location="query")
    @output(GenericSchema)
    async def delete(self,info: dict):

        print(info)
        res = await self.todoService.delete_todos(
            info["todo_ids"],
        )
        if res:
            return {"message": "successfully deleted"}
        return {"message": "no todo found"}, 404
