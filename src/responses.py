"""Стандартные HTTP json ответы."""
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
)

from src.schemas import (
    CreateScheme, NotFoundScheme, UnpassableEntityScheme, OkScheme,
    UnauthorizedScheme, BadRequestScheme
)

OkJSONResponse = JSONResponse(
    content=OkScheme().dict(),
    status_code=HTTP_200_OK,
)

CreateJSONResponse = JSONResponse(
    content=CreateScheme().dict(),
    status_code=HTTP_201_CREATED,
)

UnauthorizedResponse = JSONResponse(
    content=UnauthorizedScheme().dict(),
    status_code=HTTP_401_UNAUTHORIZED,
)

BadRequestJSONResponse = JSONResponse(
    content=BadRequestScheme().dict(),
    status_code=HTTP_400_BAD_REQUEST,
)

NotFoundJSONResponse = JSONResponse(
    content=NotFoundScheme().dict(),
    status_code=HTTP_404_NOT_FOUND,
)

UnpassableEntityJSONResponse = JSONResponse(
    content=UnpassableEntityScheme().dict(),
    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
)
