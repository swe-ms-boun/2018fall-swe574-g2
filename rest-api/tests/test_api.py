import pytest
from app import app
import os
import tempfile


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_check_available_url_annotation(client):
    rv = client.get('/')
    assert b'/add/annotation' in rv.data


def test_check_available_url_creator(client):
    rv = client.get('/')
    assert b'/add/creator' in rv.data


def test_check_creator_cannot_post(client):
    rv = client.post('/add/creator', json={
        'email': 'test@gmail.com'
    })
    print(rv.data)
    assert b'405 Method Not Allowed' in rv.data


def test_check_creator_put(client):
    rv = client.put('/add/creator', data=dict(
        email='test@gmail.com',
        home_page='home_page',
        id='5',
    ), follow_redirects=True)

    print(rv.data)
    assert b'created_time":["This field is required."]' in rv.data


def test_check_creator_get(client):
    rv = client.get('/add/creator/1', follow_redirects=True)

    print(rv.data)
    assert b'{"error":"Not found"}' in rv.data


def test_check_user_unauthorized_access(client):
    rv = client.get('/get/user/deniz', follow_redirects=True)

    print(rv.data)
    assert b'"error":"Unauthorized access"' in rv.data
