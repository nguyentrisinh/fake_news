from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.core import exceptions
from datetime import datetime, timedelta
import pytz
from rest_framework import status

from ..infrastructures import ApiCustomException
from ..constants import ErrorDefine
# from ..constants import Constant


class ExpiringTokenAuthentication(TokenAuthentication):
    # constant = Constant()

    def authenticate_credentials(self, key):
        model = self.get_model()

        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise ApiCustomException(ErrorDefine.INVALID_TOKEN, status.HTTP_401_UNAUTHORIZED)

        # if not token.user.is_active:
        #     raise ApiCustomException(ErrorDefine.USER_INACTIVE, status.HTTP_401_UNAUTHORIZED)

        # This is required for the time comparison
        utc_now = datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        # if token.created < utc_now - timedelta(seconds=self.constant.get_token_expired_time()):
        #     raise ApiCustomException(ErrorDefine.TOKEN_EXPIRED, status.HTTP_401_UNAUTHORIZED)

        return token.user, token
