from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.settings import Settings


def test_settings():
    settings = Settings()

    assert settings.DATABASE_URL is not None


def test_get_session():
    gen = get_session()
    session = next(gen)

    assert isinstance(session, Session)

    try:
        next(gen)
    except StopIteration:
        pass
