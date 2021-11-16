def register_routes(api, app, root="api"):
    from app.user import register_user_routes as attach_user

    attach_user(api, app)

