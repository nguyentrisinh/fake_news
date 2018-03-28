class ApiResponse:
    def __init__(self, data, errors):
        self.data = data
        self.errors = errors

    def get(self):
        return {
            'data': self.data,
            'errors': self.errors
        }