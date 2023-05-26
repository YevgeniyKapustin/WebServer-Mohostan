from starlette.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
)

from src.schemas import (
    OkScheme, CreateScheme, BadRequestScheme, NotFoundScheme
)


def get_get_response(scheme):
    return {
        HTTP_200_OK: {
            'model': scheme,
            'description': 'Объект получен',
        },
        HTTP_404_NOT_FOUND: {
            'model': NotFoundScheme,
            'description': 'Объект не существует',
        }
    }


def get_create_response():
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


def get_update_response():
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


def get_delete_response():
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
