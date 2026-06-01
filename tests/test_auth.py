from http import HTTPStatus


def test_get_token(client, user):

    response = client.post(
        '/auth/token', data={'username': user.email, 'password': user.clean_password}
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'bearer'
    assert 'access_token' in token


def test_get_token_invalid_email(client, user):
    response = client.post(
        '/auth/token', data={'username': 'fantasma@example.com', 'password': user.clean_password}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Email ou senha incorretos'}


def test_get_token_invalid_password(client, user):
    response = client.post(
        '/auth/token', data={'username': user.email, 'password': 'senha_claramente_falsa'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Email ou senha incorretos'}
