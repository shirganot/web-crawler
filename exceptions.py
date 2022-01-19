class TooManyRequestsError(Exception):
    def __init__(self, message="Too many requests"):
        self.message = message
        super().__init__(self.message)
