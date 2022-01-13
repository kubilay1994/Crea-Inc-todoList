from apiflask.blueprint import APIBlueprint


admin = APIBlueprint("admin", __name__)

import server.routes.admin.user