from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert 'Olá Mundo!' in response.text


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@example.com',
    }


def test_create_user_username_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'outro@email.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username de usuário já existente'}


def test_create_user_email_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'OutroNome',
            'email': 'teste@teste.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email de usuário já existente'}


def test_read_users(client, user, token):

    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_get_user_should_return_not_found(client):
    response = client.get('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_get_user(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_update_user(client, user, token):
    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'bob',
        'email': 'bob@example.com',
    }


def test_update_user_not_found(client, token):
    response = client.put(
        '/users/999',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_update_user_forbidden(client, token, other_user):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Sem permissões'}


def test_update_integrity_error(client, user, token):
    client.post(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'Username or Email já existem'}


def test_delete_user(client, user, token):
    response = client.delete('/users/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'usuário deletado'}


def test_delete_user_not_found(client, token):
    response = client.delete(
        '/users/999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_delete_user_forbidden(client, token, other_user):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Sem permissões'}


def test_get_token(client, user):

    response = client.post('/token', data={'username': user.email, 'password': user.clean_password})

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'bearer'
    assert 'access_token' in token


def test_get_token_invalid_email(client, user):
    response = client.post(
        '/token', data={'username': 'fantasma@example.com', 'password': user.clean_password}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Email ou senha incorretos'}


def test_get_token_invalid_password(client, user):
    response = client.post(
        '/token', data={'username': user.email, 'password': 'senha_claramente_falsa'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Email ou senha incorretos'}
