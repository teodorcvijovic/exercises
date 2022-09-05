from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request, status


class RecipeServerException(HTTPException):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code or 500


async def recipe_server_exception_handler(
        _: Request, e: RecipeServerException
) -> JSONResponse:
    """
    Default HTTP error handler.
    :param _: Request object
    :param e: HTTPException object
    :return: Error response
    """
    return JSONResponse(
        status_code=e.status_code,
        content={
            'title': 'Http exception raised',
            'message': e.message
        }
    )


async def generic_error_handler(_: Request, e: Exception) -> JSONResponse:
    """
    Default Exception error handler.
    :param _: Request object
    :param e: Exception object
    :return: Error response
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'title': 'An unhandled exception raised',
            'message': str(e)
        }
    )
