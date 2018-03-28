from rest_framework.response import Response
from rest_framework import status

from ..infrastructures import ApiResponse, ApiErrorMessage, ApiCustomException
from ..constants import ErrorDefine

DEFAULT_ERROR_CODE = 9999


class ApiBase:
    def __init__(self):
        pass

    def as_success(self, data, status_http=status.HTTP_200_OK):
        api_response = ApiResponse(data, None)

        return Response(
            data=api_response.get(),
            status=status_http
        )

    def as_errors(self, errors, status_http=status.HTTP_400_BAD_REQUEST):
        api_response = ApiResponse(None, errors)

        return Response(
            data=api_response.get(),
            status=status_http
        )

    def as_error(self, api_error_message, status_http=status.HTTP_400_BAD_REQUEST):
        errors = [
            api_error_message.get()
        ]

        return self.as_errors(errors, status_http)

    def as_error_code(self, message, error_code, status_http=status.HTTP_400_BAD_REQUEST):
        api_response_message = ApiErrorMessage(message, error_code)
        error = api_response_message

        return self.as_error(error, status_http)

    def as_error_message(self, message, status_http=status.HTTP_400_BAD_REQUEST):
        return self.as_error_code(message, DEFAULT_ERROR_CODE, status_http)

    # check user is anonymous
    # it can confirm which request has token or not
    # if request don't have token, out system will treats it like anonymous user that can use some special function
    # this method can do as trigger to use for some request don't need login

    # def check_anonymous(self, request):
    #     fifi_user = request.user
    #     if fifi_user.is_anonymous():
    #         raise ApiCustomException(ErrorDefine.INVALID_TOKEN)
    #     return fifi_user




