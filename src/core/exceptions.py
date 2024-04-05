class BaseError(Exception):
    base_message = "Base error"

    def __init__(self, message=base_message) -> None:
        self.message = message
        super().__init__(self.message)

class DBSessionInitError(BaseError):
    base_message = "DatabaseSessionManager is not initialized"


class DBSessionMiddlewareError(Exception):
    base_message = "DB Session is not initialized in DBSessionMiddleware"


class UserUpdateError(Exception):
    base_message = "Can't update User object that's None"

class InvalidDateError(Exception):
    base_message = "Provided date is not valid"