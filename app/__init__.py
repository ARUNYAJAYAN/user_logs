from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .status_constants import HttpStatusCode
from .response import Response

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes
    from app.user.models import User

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or 'dev'])
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


    from flask import Blueprint

    api_v1 = Blueprint('api_v1', __name__)

    api = Api(api_v1,
              title="User Logs API",
              version="0.1.0", )

    register_routes(api, app)

    app.register_blueprint(api_v1, url_prefix="/user-logs")

    @app.route("/health")
    def health():
        return Response.success({"status": "Running"}, HttpStatusCode.CREATED, "Successfully working")

    return app

