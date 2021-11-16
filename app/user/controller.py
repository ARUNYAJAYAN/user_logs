from flask import request
from flask_restx import Namespace, Resource
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt
from app.response import Response
from app.status_constants import HttpStatusCode
from app.user.schemas import UserSchema, MessageSchema, ActivityLogsSchema
from app.user.delegates import UserDelegate, AuthDelegate, MessageDelegate, ActivityLogDelegate

api = Namespace("Users", description="Namespace for Users")


@api.route('v1/user')
class CreateUser(Resource):
    """
     API for create a user
    """
    def post(self):
        payload = request.json
        try:
            validated_data = UserSchema().load(payload)
            user = UserDelegate.create_user(validated_data)
            return Response.success(UserSchema().dump(user), HttpStatusCode.OK)
        except ValidationError as err:
            return Response.error(err.messages, HttpStatusCode.BAD_REQUEST)


@api.route('v1/token')
class Login(Resource):
    """
    API for login
    """
    def post(self):
        try:
            encoded_username_password = request.headers.get('Authorization').split()[-1]
            if encoded_username_password:
                response = AuthDelegate.check_user_auth(encoded_username_password)
        except ValidationError as err:
            return Response.error(err.messages, HttpStatusCode.BAD_REQUEST)

        return Response.success({
                "token": response['token']}, HttpStatusCode.OK)


@api.route('v1/message')
class CreateMessage(Resource):
    """
     API for create a message
    """
    @jwt_required()
    def post(self):
        print()
        claims = get_jwt()
        user_id = claims.get('id')
        payload = request.json
        try:
            validated_data = MessageSchema().load(payload)
            message = MessageDelegate.create_message(validated_data, user_id)
            return Response.success(MessageSchema().dump(message), HttpStatusCode.OK)
        except ValidationError as err:
            return Response.error(err.messages, HttpStatusCode.BAD_REQUEST)

    @jwt_required()
    def get(self):

        claims = get_jwt()
        user_id = claims.get('id')
        try:
            message = MessageDelegate.list_message(user_id)
            return Response.success(MessageSchema(many=True).dump(message), HttpStatusCode.OK)
        except ValidationError as err:
            return Response.error(err.messages, HttpStatusCode.BAD_REQUEST)


@api.route('v1/message/<id>')
class UpdateMessage(Resource):
    """
     API for create a user
    """
    @jwt_required()
    def put(self, id):

        claims = get_jwt()
        user_id = claims.get('id')
        payload = request.json
        try:
            validated_data = MessageSchema().load(payload)
            message = MessageDelegate.update_message(validated_data, id)
            return Response.success(MessageSchema().dump(message), HttpStatusCode.OK)
        except ValidationError as err:
            return Response.error(err.messages, HttpStatusCode.BAD_REQUEST)

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        user_id = claims.get('id')
        try:
            MessageDelegate.delete_message(id)
            return Response.success(response_data={}, status_code=HttpStatusCode.OK, message="Deleted successfully")
        except ValidationError as err:
            return Response.error(err.messages, HttpStatusCode.BAD_REQUEST)


@api.route('v1/logs')
class ListActivityLogs(Resource):
    """
     API for list logs
    """
    @jwt_required()
    def get(self):

        claims = get_jwt()
        user = claims.get('is_admin')
        try:
            logs = ActivityLogDelegate.list_activity_logs(user)
            return Response.success(ActivityLogsSchema(many=True).dump(logs), HttpStatusCode.OK)
        except ValidationError as err:
            return Response.error(err.messages, HttpStatusCode.BAD_REQUEST)