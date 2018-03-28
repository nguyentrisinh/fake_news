from ..infrastructures import ApiErrorMessage


class ErrorDefine:
    def __init__(self):
        pass

    # Error Default: 9999

    # Error Auth: 10xx
    LOGIN_FAIL = ApiErrorMessage('login fail', 1000)


