import pytest
import fixyoutube.constants as c
from fixyoutube import app as flask_app
from fixyoutube.db import clear_cache

@pytest.fixture()
def app():
    flask_app.config.update({ "TESTING": True })
    clear_cache()
    yield flask_app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_homepage(client):
    response = client.get("/")
    assert b"youtu.be" in response.data

def test_redirect(client):
    response = client.get("/" + c.SHORT_VIDEO_ID)
    assert response.location == c.BASE_URL + c.SHORT_VIDEO_ID

def test_working_video(client):
    response = client.get("/" + c.SHORT_VIDEO_ID, headers={'User-Agent': c.TELEGRAM_USER_AGENT})
    print(response.data.decode("utf-8"))
    assert b"/proxy/" + c.SHORT_VIDEO_ID.encode("utf-8") in response.data

    response = client.get("/proxy/" + c.SHORT_VIDEO_ID)
    assert response.status_code == 200

def test_not_working_video(client):
    response = client.get("/" + c.LONG_VIDEO_ID, headers={'User-Agent': c.TELEGRAM_USER_AGENT})
    assert b"/proxy/" + c.LONG_VIDEO_ID.encode("utf-8") not in response.data
    
    response = client.get("/proxy/" + c.LONG_VIDEO_ID)
    assert response.status_code == 400
