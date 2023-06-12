from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
)


async def test_get_command_not_exist(
        async_session: AsyncClient,
):
    response = await async_session.get(
        '/api/v1/commands/',
        params={
            'command_type': 'string'
        }
    )

    assert response.status_code == HTTP_404_NOT_FOUND


async def test_create_command(
        async_session: AsyncClient,
):
    response = await async_session.post(
        '/api/v1/commands/',
        json={
            "type": "string",
            "request": "string",
            "response": "string"
        }
    )

    assert response.status_code == HTTP_201_CREATED


async def test_get_commands(
        async_session: AsyncClient,
):
    response = await async_session.get(
        '/api/v1/commands/',
        params={
            'command_type': 'string'
        }
    )

    assert response.status_code == HTTP_200_OK


async def test_update_commands(
        async_session: AsyncClient,
):
    response = await async_session.put(
        '/api/v1/commands/{id}',
        params={
            'id_': 1,
        },
        json={
            'type': 'new_type'
        }
    )

    assert response.status_code == HTTP_200_OK


async def test_update_commands_not_found(
        async_session: AsyncClient,
):
    response = await async_session.put(
        '/api/v1/commands/{id}',
        params={
            'id_': 2,
        },
        json={
            'type': 'new_type'
        }
    )

    assert response.status_code == HTTP_404_NOT_FOUND


async def test_update_commands_old_obj(
        async_session: AsyncClient,
):
    response = await async_session.put(
        '/api/v1/commands/{id}',
        params={
            'id_': 1,
        },
        json={
            'type': 'string'
        }
    )

    assert response.status_code == HTTP_400_BAD_REQUEST


async def test_delete_commands(
        async_session: AsyncClient,
):
    response = await async_session.delete(
        '/api/v1/commands/',
        params={
            'command_id': 1
        }
    )

    assert response.status_code == HTTP_200_OK


async def test_delete_commands_not_exist(
        async_session: AsyncClient,
):

    response = await async_session.delete(
        '/api/v1/commands/',
        params={
            'command_id': 1
        }
    )

    assert response.status_code == HTTP_404_NOT_FOUND
