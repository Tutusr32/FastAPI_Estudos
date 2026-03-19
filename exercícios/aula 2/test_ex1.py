#Crie um novo endpoint em fast_zero/app.py que retorne "olá mundo" usando HTML e escreva seu teste em tests/test_app.py.


from http import HTTPStatus

def test_exercicio_ola_mundo_em_html(client):
    response = client.get('/exercicio-html')

    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá Mundo </h1>' in response.text
    