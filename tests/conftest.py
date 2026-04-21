from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()
    # limpa após o teste


@contextmanager
def _mock_db_time(*, model, time=datetime.now()):

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time

        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)  # registra o hook

    yield time

    event.remove(model, 'before_insert', fake_time_hook)  # remove após o bloco with


@pytest.fixture
def mock_db_time():
    return _mock_db_time  # retorna a função, não o resultado dela


@pytest.fixture
def user(session):

    user = User(username='Teste', email='teste@teste.com', password='testtest')

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
