from typing import Optional


class StatusCode:
    HTTP_500 = 500
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_405 = 405


class CommonException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

    def __repr__(self) -> dict:
        return {"status_code": self.status_code, "content": self.detail}

    def __str__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name} : {self.detail}"


class APIException(Exception):
    status_code: int
    code: str
    msg: str
    detail: str
    ex: Optional[Exception]

    def __init__(
        self,
        *,
        status_code: int = StatusCode.HTTP_500,
        code: str = "00000",
        detail: str = "",
        ex: Optional[Exception] = None,
    ):
        self.status_code = status_code
        self.code = code
        self.detail = detail
        self.ex = ex
        super().__init__(ex)


class BadRequestException(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            code=f"{StatusCode.HTTP_400}{'1'.zfill(4)}",
            detail="Bad Request Error",
            ex=ex,
        )


class ValidationException(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            code=f"{StatusCode.HTTP_400}{'1'.zfill(4)}",
            detail="Validation Error",
            ex=ex,
        )


class NotFoundException(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_404,
            code=f"{StatusCode.HTTP_404}{'1'.zfill(4)}",
            detail="Not Found Error",
            ex=ex,
        )


class AuthenticationException(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            code=f"{StatusCode.HTTP_401}{'1'.zfill(4)}",
            detail="Authentication Error",
            ex=ex,
        )
  