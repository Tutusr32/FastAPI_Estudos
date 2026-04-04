from fast_zero.settings import Settings


def test_settings():
    settings = Settings()

    assert settings.DATABASE_URL is not None
