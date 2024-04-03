class DBSessionInitError(Exception):
    detail = "DatabaseSessionManager is not initialized"

    def __init__(self, message=detail) -> None:
        super().__init__(message)