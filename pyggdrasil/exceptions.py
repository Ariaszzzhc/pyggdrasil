class ForbiddenOperationException(Exception):
    def __init__(self, error_message):
        super()
        self.error_message = error_message

    def __str__(self):
        return self.error_message


class IllegalArgumentException(Exception):
    def __init__(self, error_message):
        super()
        self.error_message = error_message

    def __str__(self):
        return self.error_message
