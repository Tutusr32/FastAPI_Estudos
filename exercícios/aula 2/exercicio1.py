#Crie um novo endpoint em fast_zero/app.py que retorne "olá mundo" usando HTML e escreva seu teste em tests/test_app.py.

from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

from fastapi.responses import HTMLResponse

app = FastAPI(title='API32')
database = []

@app.get('/exercicio-html', response_class=HTMLResponse)
def exercicio_aula_02():
    return """
    <html>
      <head>
        <title>Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>"""
