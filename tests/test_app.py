from app import app


def test_app_exists():
    assert app is not None


def test_app_has_name():
    assert app.name == "app"