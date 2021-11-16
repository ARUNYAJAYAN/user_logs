from app import db
from app.user.models import User, Message, ActivityLog
from werkzeug.security import generate_password_hash, check_password_hash
from app.exceptions import UserAlreadyExist, InvalidUser


class UserService:
    @staticmethod
    def create_user(data):
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            raise UserAlreadyExist()

        password_hash = generate_password_hash(data["password"], method='sha256')
        data["password"] = password_hash

        user = User(**data)
        db.session.add(user)
        db.session.commit()
        ActivityLogService.create_logs(user, activity="SignUp")
        return user


class AuthService:

    @staticmethod
    def login(data):
        user = User.query.filter_by(email=data["username"]).first()
        if not user:
            raise InvalidUser()

        if not check_password_hash(user.password, data["password"]):
            raise InvalidUser()

        token = user.encode_auth_token(data)

        ActivityLogService.create_logs(user, activity="SignIn")
        return {
            "token": token
        }


class MessageService:
    @staticmethod
    def create_message(data, user_id):
        existing_user = User.query.filter_by(id=user_id).first()
        data["user_id"] = user_id

        message = Message(**data)
        db.session.add(message)
        db.session.commit()
        ActivityLogService.create_logs(message, activity="Create_message")
        return message

    @staticmethod
    def list_message(user_id):
        message = Message.query.filter_by(user_id=user_id).all()
        ActivityLogService.create_logs(message[0], activity="List_message")
        return message

    @staticmethod
    def update_message(data, id):
        message = Message.query.filter_by(id=id).first()

        for field, value in data.items():
            setattr(message, field, value)
        db.session.commit()
        ActivityLogService.create_logs(message, activity="Update_message")
        return message

    @staticmethod
    def delete_message(id):
        message = Message.query.filter_by(id=id).first()
        ActivityLogService.create_logs(message, activity="Delete_message")
        Message.query.filter_by(id=id).delete()
        db.session.commit()


class ActivityLogService:
    @staticmethod
    def create_logs(user, activity):
        data = {}
        if activity == "SignUp":
            data['user_id'] = user.id
            data['activity'] = str(user.full_name + "sign up")
        elif activity == "SignIn":
            print("hdbjfhfd")
            data['user_id'] = user.id
            data['activity'] = str(user.full_name + " signed in")
        elif activity == "Create_message":
            data['user_id'] = user.user.id
            data['activity'] = str(user.user.full_name + " created a message")
        elif activity == "List_message":
            data['user_id'] = user.user.id
            data['activity'] = str(user.user.full_name + " list messages")
        elif activity == "Update_message":
            data['user_id'] = user.user.id
            data['activity'] = str(user.user.full_name + " update a message")
        elif activity == "Delete_message":
            data['user_id'] = user.user.id
            data['activity'] = str(user.user.full_name + " deleted a message")
        log = ActivityLog(**data)
        db.session.add(log)
        db.session.commit()
        return log

    @staticmethod
    def list_activity_logs(user):
        if user:
            logs = ActivityLog.query.all()
        else:
            logs=[]
        return logs