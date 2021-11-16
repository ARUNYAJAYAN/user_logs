import datetime
from app import db
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy.orm import backref, relationship


class User(db.Model):
    """
    A user model
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    is_admin = db.Column(db.Boolean, default=False)

    def get_auth_token(self, data):

        payload = {
            "id": self.id,
            "email": self.email,
            "is_admin": self.is_admin
        }

        token = create_access_token(
            self.email,
            additional_claims=payload
        )
        return token

    def get_refresh_token(self):

        return create_refresh_token(identity=self.email)

    def encode_auth_token(self, data):

        # try:

        token = self.get_auth_token(data)

        refresh_token = self.get_refresh_token()

        return {
            "access": token,
            "refresh": refresh_token
        }


class Message(db.Model):
    """
    A message model
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    user = relationship("User", foreign_keys=[user_id])


class ActivityLog(db.Model):
    """
    For storing activity log
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_on = db.Column(db.DateTime, default=db.func.now())
    user = relationship("User", foreign_keys=[user_id])
