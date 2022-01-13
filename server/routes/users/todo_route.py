from typing import Optional
from apiflask.blueprint import APIBlueprint
from apiflask.decorators import doc, output
from lagom.decorators import magic_bind_to_container
from server.schemas.todo import TodoOutSchema

from server.utils import register_rest_view

from server.views import TodoView

from main import dep_container
from app.services.todos.TodoService import TodoService


user_todo_route = APIBlueprint("user", __name__)
register_rest_view(user_todo_route, TodoView)


@user_todo_route.get("/todos")
@output(TodoOutSchema(many=True))
@doc(
    summary="Gets all todo items",
    description=" Gets todo items owned by user",
)
@magic_bind_to_container(container=dep_container)
async def get(user_id: int, todoService: TodoService):
    res = await todoService.get_user_todos(user_id)
    return res
