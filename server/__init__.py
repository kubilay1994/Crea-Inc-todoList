from apiflask import APIFlask

from flask_cors import CORS
from lagom.definitions import Singleton
from sqlalchemy.ext.asyncio import async_scoped_session


from app.db import db_session
from app.db import init_db

from lagom import Container


from app.services import UserService, TodoService, TokenService, RoleService

from app.repos import TodoRepo, UserRepo, RoleRepo


def create_container():
    container = Container()
    container[TokenService] = Singleton(TokenService)
    container[async_scoped_session] = db_session

    container[TodoRepo] = Singleton(TodoRepo)
    container[TodoService] = Singleton(TodoService)

    container[UserRepo] = Singleton(UserRepo)
    container[UserService] = Singleton(UserService)
    container[RoleRepo] = Singleton(RoleRepo)
    container[RoleService] = RoleService

    return container


async def create_app():

    init_db()

    app = APIFlask(
        __name__,
        json_errors=True,
        title="Flask Todo Application with swagger support",
        version="0.1",
    )
    cors = CORS()
    cors.init_app(app)

    @app.teardown_appcontext
    async def shutdown_session(exception=None):
        await db_session.remove()

    return app
