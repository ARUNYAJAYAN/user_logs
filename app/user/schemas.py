from app import ma, db
from marshmallow import post_load, fields, validate
from .models import User, Message, ActivityLog


class UserSchema(ma.SQLAlchemySchema):
    id = fields.Integer(dump_only=True)
    full_name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    is_active = fields.Boolean(dump_only=True)


class MessageSchema(ma.SQLAlchemySchema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    message = fields.Str(required=True)


class ActivityLogsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ActivityLog
        fields = ["id", "activity", "user_id", "created_on"]