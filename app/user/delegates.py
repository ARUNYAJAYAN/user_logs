from .services import UserService, AuthService, MessageService, ActivityLogService
import base64


class UserDelegate:

    @staticmethod
    def create_user(data):
        user = UserService.create_user(data)
        return user


class AuthDelegate:
    @staticmethod
    def check_user_auth(encoded_username_password):
        if encoded_username_password:
            auth_string = base64.b64decode(encoded_username_password).decode('utf-8')
            username, password = auth_string.split(":")
            data = {}
            data['username'] = username
            data['password'] = password
            data = AuthService.login(data)
            return data
        else:
            return None


class MessageDelegate:
    @staticmethod
    def create_message(data, user_id):
        message = MessageService.create_message(data, user_id)
        return message

    @staticmethod
    def list_message(user_id):
        message = MessageService.list_message(user_id)
        return message

    @staticmethod
    def update_message(data, id):
        message = MessageService.update_message(data, id)
        return message

    @staticmethod
    def delete_message(id):
        message = MessageService.delete_message(id)
        return message


class ActivityLogDelegate:
    @staticmethod
    def list_activity_logs(user):
        logs = ActivityLogService.list_activity_logs(user)
        return logs