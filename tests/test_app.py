from backend.config import create_app

def test_app_runs():
    app = create_app()
    assert app is not None