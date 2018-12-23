# coding=utf-8
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


def test_check_available_url_add_annotation(client):
    rv = client.get('/')
    assert b'/add/annotation' in rv.data


def test_check_available_url_add_creator(client):
    rv = client.get('/')
    assert b'/add/creator' in rv.data


def test_check_available_url_add_creator_id(client):
    rv = client.get('/')
    assert b'/get/creator/<id>' in rv.data


def test_check_available_url_get_creator_list(client):
    rv = client.get('/')
    assert b'/get/creator/list' in rv.data


def test_check_available_url_update_creator(client):
    rv = client.get('/')
    assert b'/update/creator' in rv.data


def test_check_available_url_delete_annotation(client):
    rv = client.get('/')
    assert b'/delete/annotation/<id>' in rv.data


def test_check_available_url_get_annotation(client):
    rv = client.get('/')
    assert b'/get/annotation/<id>' in rv.data


def test_check_available_url_get_annotations(client):
    rv = client.get('/')
    assert b'/get/annotations/<ids>' in rv.data


def test_check_available_url_get_annotation_by_target_id(client):
    rv = client.get('/')
    assert b'/get/annotation/target/<id>' in rv.data


def test_check_add_creator_with_post(client):
    rv = client.post('/add/creator', json={
        'email': 'test@gmail.com'
    })
    assert b'405 Method Not Allowed' in rv.data


def test_check_add_creator(client):
    rv = client.put('/add/creator', data=dict(
        email='test@gmail.com',
        home_page='home_page',
        id='5',
    ), follow_redirects=True)
    assert b'Creator created successfully!' in rv.data


def test_check_add_creator_without_mail(client):
    rv = client.put('/add/creator', data=dict(
        home_page='home_page',
        id='5',
    ), follow_redirects=True)
    assert b'Ops, creator could not be created!' in rv.data


def test_check_add_creator_without_id(client):
    rv = client.put('/add/creator', data=dict(
        email='test@gmail.com',
        home_page='home_page',
    ), follow_redirects=True)
    assert b'Ops, creator could not be created!' in rv.data


def test_check_add_creator_without_home_page(client):
    rv = client.put('/add/creator', data=dict(
        email='test@gmail.com',
        id='5',
    ), follow_redirects=True)
    assert b'Ops, creator could not be created!' in rv.data


def test_check_add_creator_already(client):
    rv = client.put('/add/creator', data=dict(
        email='test@gmail.com',
        home_page='home_page',
        id='5',
    ), follow_redirects=True)
    assert b'Ops, this email is already taken' in rv.data

# Different options should be written like instead of writing email, write int.
# Instead of writing int id, write string ...
# get_spesific_creator_by_id methods should be written.


def test_check_creator_get(client):
    rv = client.get('/add/creator/1', follow_redirects=True)

    print(rv.data)
    assert b'{"error":"Not found"}' in rv.data


def test_check_user_unauthorized_access(client):
    rv = client.get('/get/user/deniz', follow_redirects=True)

    print(rv.data)
    assert b'"error":"Unauthorized access"' in rv.data
