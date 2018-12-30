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


# Add creator tests
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


def test_check_add_creator_string_id(client):
    # Failed. User created with string id "a". Issue opened
    rv = client.put('/add/creator', data=dict(
        email='test@gmail.com',
        home_page='home_page',
        id='a',
    ), follow_redirects=True)
    assert b'Ops, creator could not be created!' in rv.data


def test_check_add_creator_invalid_email(client):
    # Failed. User created with invalid email address "test". Issue opened
    rv = client.put('/add/creator', data=dict(
        email='test',
        home_page='home_page',
        id=3,
    ), follow_redirects=True)
    assert b'Ops, creator could not be created!' in rv.data


def test_check_add_creator_invalid_homepage(client):
    # Failed. User created with invalid homepage "home_page". Issue opened
    rv = client.put('/add/creator', data=dict(
        email='test',
        home_page='home_page',
        id=3,
    ), follow_redirects=True)
    assert b'Ops, creator could not be created!' in rv.data


# get_spesific_creator_by_id tests.
def test_check_get_creator_by_id(client):
    rv = client.get('/get/creator/1')
    assert '200' in rv.status


def test_check_get_creator_by_id_created_time(client):
    rv = client.get('/get/creator/1')
    assert 'created_time' in rv.data


def test_check_get_creator_by_id_email(client):
    rv = client.get('/get/creator/1')
    assert 'email' in rv.data


def test_check_get_creator_by_id_email_sha1(client):
    rv = client.get('/get/creator/1')
    assert 'email_sha1' in rv.data


def test_check_get_creator_by_id_home_page(client):
    rv = client.get('/get/creator/1')
    assert 'home_page' in rv.data


def test_check_get_creator_by_id_unknown_user(client):
    rv = client.get('/get/creator/66')
    assert '404' in rv.status


def test_check_get_creator_by_id_with_string_id(client):
    # Test fails. Issue opened.
    rv = client.get('/get/creator/adana')
    assert '404' in rv.status


# Test get/creator/list/ endpoint
def test_check_get_all_creators(client):
    rv = client.get('/get/creator/list')
    assert '200' in rv.status


# Test update/creator endpoint
def test_check_update_creator_add_nick(client):
    rv = client.post('/update/creator', data=dict(
        nick='mk0730',
        email='mehmet.kayaalp@boun.edu.tr',
        id=3,
    ), follow_redirects=True)
    assert "200" in rv.status


def test_check_update_creator_change_email(client):
    rv = client.post('/update/creator', data=dict(
        email='mehmet.kayaalp@ozu.edu.tr',
        id=3,
    ), follow_redirects=True)
    assert "200" in rv.status


def test_check_update_creator_change_email(client):
    rv = client.post('/update/creator', data=dict(
        home_page='http://thymesis.com/mk0730',
        id=3,
    ), follow_redirects=True)
    assert "200" in rv.status


def test_check_update_creator_change_email_sha1(client):
    # When changing email, the sha1 should also be change.
    # This is wrong and should be changed.
    # Issue opened.
    rv = client.post('/update/creator', data=dict(
        home_page='http://thymesis.com/mk0730',
        id=3,
    ), follow_redirects=True)
    assert "200" in rv.status


def test_check_update_unknown_creator_without_email(client):
    # Yasser user does not exist now.
    rv = client.post('/update/creator', data=dict(
        home_page='http://thymesis.com/yasser',
        id=10,
    ), follow_redirects=True)
    assert "404" in rv.status


def test_check_update_unknown_creator_without_id(client):
    # Yasser user does not exist now.
    rv = client.post('/update/creator', data=dict(
        home_page='http://thymesis.com/yasser',
        email="yasser@gmail.com"
    ), follow_redirects=True)
    assert "404" in rv.status


def test_check_update_unknown_creator_without_home_page(client):
    #  Yasser user does not exist now.
    rv = client.post('/update/creator', data=dict(
        id=10,
        email="yasser@gmail.com"
    ), follow_redirects=True)
    assert "404" in rv.status


def test_check_update_unknown_creator_with_all_new_info(client):
    rv = client.post('/update/creator', data=dict(
        home_page='http://thymesis.com/yasser',
        id=10,
        email="yasser@gmail.com"
    ), follow_redirects=True)
    assert "200" in rv.status


def test_check_creator_get(client):
    rv = client.get('/add/creator/1', follow_redirects=True)

    print(rv.data)
    assert b'{"error":"Not found"}' in rv.data


def test_check_user_unauthorized_access(client):
    rv = client.get('/get/user/deniz', follow_redirects=True)

    print(rv.data)
    assert b'"error":"Unauthorized access"' in rv.data


# add annotation tests will be written