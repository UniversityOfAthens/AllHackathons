import pytest
from main import app as flask_app, db

@pytest.fixture()
def app():
    flask_app.config.update({
        "TESTING": True,
    })

    with flask_app.app_context():
        yield flask_app
        db.session.remove()  # It deletes stored cache and cleans up the db so there are no conflicts
        db.drop_all()  # After each test is completed it completely deletes db schema & table.

@pytest.fixture()
def client(app):
    return app.test_client()