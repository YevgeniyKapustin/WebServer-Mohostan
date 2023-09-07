"""Глобальные константы."""
from pydantic import BaseModel
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_418_IM_A_TEAPOT
)

from src.schemas import (
    CreateScheme, NotFoundScheme, UnpassableEntityScheme, OkScheme,
    UnauthorizedScheme, BadRequestScheme, HTTPExceptionScheme
)


# стандартные pydantic ответы
def get_get_response(scheme) -> dict:
    return {
        HTTP_200_OK: {
            'model': list[scheme],
            'description': 'Объект получен',
        },
        HTTP_404_NOT_FOUND: {
            'model': NotFoundScheme,
            'description': 'Объект не существует',
        }
    }


def get_create_response() -> dict:
    return {
        HTTP_200_OK: {
            'model': OkScheme,
            'description': 'Объект уже существует',
        },
        HTTP_201_CREATED: {
            'model': CreateScheme,
            'description': 'Объект создан',
        }
    }


def get_update_response() -> dict:
    return {
        HTTP_200_OK: {
            'model': OkScheme,
            'description': 'Объект изменен',
        },
        HTTP_201_CREATED: {
            'model': CreateScheme,
            'description': 'Объект создан',
        },
        HTTP_400_BAD_REQUEST: {
            'model': BadRequestScheme,
            'description': 'Конечный объект уже существует'
        },
    }


def get_delete_response() -> dict:
    return {
        HTTP_200_OK: {
            'model': OkScheme,
            'description': 'Объект удален',
        },
        HTTP_404_NOT_FOUND: {
            'model': NotFoundScheme,
            'description': 'Объект не существует',
        },
    }


# специфические pydantic ответы
def get_video_create_response():
    response: dict = get_create_response()
    response[HTTP_418_IM_A_TEAPOT] = {
        'model': HTTPExceptionScheme,
        'detail': 'Файл должен быть mp4'
    }
    return response


# Стандартные json ответы
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
