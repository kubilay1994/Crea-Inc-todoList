from apiflask import APIBlueprint
from werkzeug.exceptions import NotFound

from apiflask import input


from core.entities.user import User
from app.services.auth.UserService import UserService


from main import dep_container
from lagom.decorators import magic_bind_to_container
from apiflask.decorators import output
from server.schemas import UserOutSchema, UserSchema, TokenInfoSchema, RegisterSchema
from app.services.roles.role import RoleService


user_route = APIBlueprint("users", __name__)


@user_route.post("/login")
@input(UserSchema)
@output(TokenInfoSchema)
@magic_bind_to_container(container=dep_container)
async def login(user: dict, user_service: UserService):
    res = await user_service.login(User(**user))
    if res is None:
        raise NotFound
    return res


@user_route.post("/register")
@input(RegisterSchema)
@output(UserOutSchema)
@magic_bind_to_container(container=dep_container)
async def register(user: dict, user_service: UserService, role_service: RoleService):

    roles = await role_service.get_roles()

    role_name = "admin" if user["is_admin"] else "basic"
    user["role_id"] = next(filter(lambda e: e.name == role_name, roles)).id
    user.pop("is_admin", None)
    created = await user_service.register(User(**user))
    return {
        "id": created.id,
        "username": created.username,
        "message": "user created successfully",
    }
