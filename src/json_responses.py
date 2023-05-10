"""Стандартные HTTP json ответы."""
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY, HTTP_401_UNAUTHORIZED
)

from src.schemas import (
    CreateScheme, NotFoundScheme, UnpassableEntityScheme, OkScheme,
    UnauthorizedScheme
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

NotFoundJSONResponse = JSONResponse(
    content=NotFoundScheme().dict(),
    status_code=HTTP_404_NOT_FOUND,
)

UnpassableEntityJSONResponse = JSONResponse(
    content=UnpassableEntityScheme().dict(),
    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
)
