#Crie um endpoint de GET para pegar um único recurso como users/{id} e fazer seus testes para 200 e 404.

from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI(title='API32')
database = []

@app.get('/users/{id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def exercicio(id: int):
    if id > len(database) or id <= 0:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')

    return database[id - 1]
