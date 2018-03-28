class ApiErrorMessage:
    def __init__(self, error_message, error_code):
        self.error_message = error_message
        self.error_code = error_code

    def get(self):
        return {
            'errorMessage': self.error_message,
            'errorCode': self.error_code
        }