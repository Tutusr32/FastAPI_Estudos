#Crie um endpoint de GET para pegar um único recurso como users/{id} e fazer seus testes para 200 e 404.

from http import HTTPStatus

def test_exercicio(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
                'username': 'alice',
                'email': 'alice@example.com',
                'id': 1,
                }


def test_exercicio_not_found(client):
    response = client.get('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}
