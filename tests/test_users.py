from httpx import AsyncClient


async def test_new_register(async_session: AsyncClient):
    response = await async_session.post(
        '/api/v1/auth/registration',
        json={
            'email': 'dev@test.com',
            'password': 'superpass',
        }
    )

    assert response.status_code == 201


async def test_register_already_exist(async_session: AsyncClient):
    response = await async_session.post(
        '/api/v1/auth/registration',
        json={
            'email': 'dev@test.com',
            'password': 'superpass',
        }
    )

    assert response.status_code == 400


async def test_login(async_session: AsyncClient):
    response = await async_session.post(
        '/api/v1/auth/login',
        data={
            'grant_type': None,
            'username': 'dev@test.com',
            'password': 'superpass',
            'scope': None,
            'client_id': None,
            'client_secret': None
        }
    )

    assert response.status_code == 200
