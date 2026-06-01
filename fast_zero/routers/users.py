from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import FilterPage, Message, UserList, UserPublic, UserSchema
from fast_zero.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix='/users', tags=['users'])

SessionDep = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(session: SessionDep, user: UserSchema):

    db_user = session.scalar(
        select(User).where((User.username == user.username) | (User.email == user.email))
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Username de usuário já existente'
            )

        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email de usuário já existente'
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    session: SessionDep,
    current_user: CurrentUser,
    filter_users: Annotated[FilterPage, Query()],
):

    users = session.scalars(select(User).limit(filter_users.limit).offset(filter_users.skip))

    return {'users': users}


@router.get('/{user_id}', response_model=UserPublic)
def read_user_by_id(session: SessionDep, user_id: int):

    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado')

    return db_user


@router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(
    session: SessionDep,
    current_user: CurrentUser,
    user_id: int,
    user: UserSchema,
):

    db_user = session.get(User, user_id)

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado')

    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Sem permissões')

    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)

        session.add(db_user)
        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Username or Email já existem')


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    session: SessionDep,
    current_user: CurrentUser,
    user_id: int,
):
    db_user = session.get(User, user_id)

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado')

    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Sem permissões')

    session.delete(db_user)
    session.commit()

    return {'message': 'usuário deletado'}
