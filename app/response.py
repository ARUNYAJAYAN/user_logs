from .status_constants import HttpStatusCode


class Response:
    """
    Common class to manage all response
    """
    @staticmethod
    def success(response_data, status_code=HttpStatusCode, message="Success"):
        """
        Method to return a common format success response
        :param response_data:
        :param status_code:
        :param message:
        :return:
        """
        if not isinstance(status_code, HttpStatusCode):
            raise TypeError('status_code must be an instance of HttpStatusCode Enum')

        return {
            "status": status_code.name,
            "code": status_code.value,
            "response_data": response_data,
            "message": message
        }, status_code.value

    @staticmethod
    def error(error_data, status_code=None, message="Error"):
        """
        Method to return a common format for error response.
        :param error_data:
        :param status_code:
        :param message:
        :return:
        """
        if not isinstance(status_code, HttpStatusCode):
            raise TypeError('status_code must be an instance of HttpStatusCode Enum')

        if business_error is not None and not isinstance(business_error, BusinessErrorCode):
            raise TypeError('business_error mus be an instance of BusinessErrorCode Enum')

        error_response = {
            "status": status_code.name,
            "code": status_code.value,
            "error_data": error_data,
            "message": message
        }

        return error_response, status_code.value

