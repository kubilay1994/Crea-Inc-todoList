from typing import Type, Union
from flask.views import MethodView
from apiflask import APIFlask, APIBlueprint


def register_rest_view(app: Union[APIFlask, APIBlueprint], cls: Type[MethodView]):

    name = cls.__name__.lower().replace("view", "")
    name_plural = f"{name}s"
    view_func = cls.as_view(name)

    app.add_url_rule(
        f"/{name_plural}/<int:{name}_id>",
        view_func=view_func,
        methods=["GET", "PUT", "DELETE", "PATCH"],
    )

    app.add_url_rule(
        f"/{name_plural}",
        view_func=view_func,
        methods=["POST"],
    )

  
