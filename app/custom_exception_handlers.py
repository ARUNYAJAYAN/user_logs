from app.response import Response
from app.exceptions import (
    UserAlreadyExist, InvalidUser
)
from app.status_constants import HttpStatusCode


def register_error_handlers(api):

    @api.errorhandler(UserAlreadyExist)
    def handle_user_already_exist_exception(error):
        return Response.error(
            {"exception": str(error)},
            HttpStatusCode.BAD_REQUEST,
            message=str(error)
        )

    @api.errorhandler(InvalidUser)
    def handle_invalid_user(error):
        return Response.error(
            {"exception": str(error)},
            HttpStatusCode.BAD_REQUEST,
            message=str(error)
        )
