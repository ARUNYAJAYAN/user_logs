def register_user_routes(api, app, root="api"):
    from .controller import api as user_api
    api.add_namespace(user_api, path=f"/")