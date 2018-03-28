from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework import status


class ApiCustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid custom')
    default_code = 'invalid custom'

    def __init__(self, api_error_message, status_code=status.HTTP_400_BAD_REQUEST):
        self.detail = api_error_message.get()
        self.status_code = status_code

    def __str__(self):
        return str(self.detail.get())
