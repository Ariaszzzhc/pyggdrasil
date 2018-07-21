class PYggdrasilException(Exception):
    def __init__(self, error, error_message, status, payload=None):
        super().__init__()
        self.error = error
        self.error_message = error_message,
        self.error_message = self.error_message[0]
        self.status = status,
        self.status = self.status[0]
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.error
        rv['errorMessage'] = self.error_message
        return rv


class ForbiddenOperationException(PYggdrasilException):
    def __init__(self, error_message):
        super().__init__("ForbiddenOperationException", error_message, 403)


class IllegalArgumentException(PYggdrasilException):
    def __init__(self, error_message):
        super().__init__("IllegalArgumentException", error_message, 400)


class AlreadyExistException(PYggdrasilException):
    def __init__(self, error_message):
        super().__init__("AlreadyExistException", error_message, 409)
