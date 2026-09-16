class AppError(Exception):
    """Domain error raised by services and mapped to an HTTP response."""

    def __init__(self, status_code: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message


class EmailAlreadyRegisteredError(AppError):
    def __init__(self) -> None:
        super().__init__(409, "email_taken", "An account with this email already exists.")


class InvalidCredentialsError(AppError):
    def __init__(self) -> None:
        super().__init__(401, "invalid_credentials", "Invalid email or password.")


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Authentication required.") -> None:
        super().__init__(401, "unauthorized", message)


class NotFoundError(AppError):
    def __init__(self, message: str = "Resource not found.") -> None:
        super().__init__(404, "not_found", message)


class ConflictError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(409, "conflict", message)


class ForbiddenError(AppError):
    def __init__(self, message: str = "You do not have access to this resource.") -> None:
        super().__init__(403, "forbidden", message)
