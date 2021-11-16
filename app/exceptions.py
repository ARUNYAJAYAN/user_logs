from .response import Response


class UserAlreadyExist(Exception):

    def __init__(self, message="User already exists"):
        self.message = message

        super().__init__(self.message)


class InvalidUser(Exception):

    def __init__(self, message="Invalid username or password"):
        self.message = message

        super().__init__(self.message)

