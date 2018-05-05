from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from ..infrastructures import ApiErrorMessage, ApiCustomException


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {'data': None}

        type_exc = type(exc)

        errors = []

        # if ValidationError
        if type_exc is ValidationError:
            for key, value in exc.detail.iteritems():
                error_message = '{}: {}'.format(key, value[0])
                api_error_message = ApiErrorMessage(error_message, 9999)
                errors.append(api_error_message.get())
            # for key in list(exc.detail.keys()):
            #     value = exc.detail[key]
            #     error_message = '{}: {}'.format(key, value[0])
            #     api_error_message = ApiErrorMessage(error_message, 9999)
            #     errors.append(api_error_message.get())

        elif type_exc is ApiCustomException:
            errors.append(exc.detail)
        else:
            api_error_message = ApiErrorMessage(str(exc), 9999)
            errors.append(api_error_message.get())

        response.data['errors'] = errors
    return response


# def custom_exception_handler(exc, context):
#     # Call REST framework's default exception handler first,
#     # to get the standard error response.
#     response = exception_handler(exc, context)
#
#     # Now add the HTTP status code to the response.
#     if response is not None:
#         response.data['status_code'] = response.status_code
#
#     return response
