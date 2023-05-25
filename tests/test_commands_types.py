from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
)


async def test_get_type_not_exist(
        async_session: AsyncClient,
        get_superuser_token_headers: dict
):
    id = 1
    response = await async_session.get(
        f'/api/v1/types/{id}',
        headers=get_superuser_token_headers
    )

    assert response.status_code == HTTP_404_NOT_FOUND


async def test_create_type(
        async_session: AsyncClient,
        get_superuser_token_headers: dict
):
    response = await async_session.post(
        f'/api/v1/types/',
        headers=get_superuser_token_headers,
        params={
            'name': 'Тестовый тип',
        }
    )

    assert response.status_code == HTTP_201_CREATED


async def test_create_type_already_exist(
        async_session: AsyncClient,
        get_superuser_token_headers: dict
):
    response = await async_session.post(
        f'/api/v1/types/',
        headers=get_superuser_token_headers,
        params={
            'name': 'Тестовый тип',
        }
    )

    assert response.status_code == HTTP_200_OK


async def test_get_type(
        async_session: AsyncClient,
        get_superuser_token_headers: dict
):
    id = 1
    response = await async_session.get(
        f'/api/v1/types/{id}',
        headers=get_superuser_token_headers,
    )

    assert response.status_code == HTTP_200_OK


async def test_update_type(
        async_session: AsyncClient,
        get_superuser_token_headers: dict
):
    id = 1
    response = await async_session.put(
        f'/api/v1/types/',
        headers=get_superuser_token_headers,
        data={
            'id': id,
        },
        params={
            'name': 'Измененный тестовый тип'
        }
    )

    assert response.status_code == HTTP_200_OK


async def test_update_type_new_obj(
        async_session: AsyncClient,
        get_superuser_token_headers: dict
):
    id = 2
    response = await async_session.put(
        f'/api/v1/types/',
        headers=get_superuser_token_headers,
        data={
            'id': id,
        },
        params={
            'name': 'Новый тип'
        }
    )

    assert response.status_code == HTTP_201_CREATED


async def test_update_type_old_obj(
        async_session: AsyncClient,
        get_superuser_token_headers: dict
):
    id = 1
    response = await async_session.put(
        f'/api/v1/types/',
        headers=get_superuser_token_headers,
        data={
            'id': id,
        },
        params={
            'name': 'Новый тип'
        }
    )

    assert response.status_code == HTTP_400_BAD_REQUEST


async def test_delete_type(
        async_session: AsyncClient,
        get_superuser_token_headers: dict
):
    id = 1
    response = await async_session.delete(
        f'/api/v1/types/',
        headers=get_superuser_token_headers,
        params={
            'id': id
        }
    )

    assert response.status_code == HTTP_200_OK


async def test_delete_type_not_exist(
        async_session: AsyncClient,
        get_superuser_token_headers: dict
):
    id = 1
    response = await async_session.delete(
        f'/api/v1/types/',
        headers=get_superuser_token_headers,
        params={
            'id': id
        }
    )

    assert response.status_code == HTTP_404_NOT_FOUND
