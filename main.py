import asyncio
from apiflask.blueprint import APIBlueprint
from dotenv import load_dotenv
from server import create_app, create_container


from server.utils import register_rest_view


async def main():
    load_dotenv()
    app = await create_app()
    return app


app = asyncio.run(main())
dep_container = create_container()


from server.routes import user_route, user_todo_route

# import views after app init
import server.views as views

from server.views.admin.todo import admin


user_route.register_blueprint(user_todo_route, url_prefix="<int:user_id>")


app.register_blueprint(user_route, url_prefix="/users")
app.register_blueprint(admin, url_prefix="/admin")
