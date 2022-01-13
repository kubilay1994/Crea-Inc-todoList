from apiflask import output
from lagom import magic_bind_to_container
from server.routes.admin import admin
from app.services.auth.UserService import UserService
from server.schemas.user import UserInfoSchema

from main import dep_container


@admin.get("/users")
@output(UserInfoSchema(many=True))
@magic_bind_to_container(container=dep_container)
async def login(user_service: UserService):
    res = await user_service.get_users()
    return res
