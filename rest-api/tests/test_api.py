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
    rv = client.put('/add/creator', data=dict(
        email='test',
        home_page='home_page',
        id=3,
    ), follow_redirects=True)
    assert b'The email is not in a valid format.' in rv.data


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


def test_check_update_creator_with_invalid_email(client):
    rv = client.post('/update/creator', data=dict(
        home_page='http://thymesis.com/mk0730',
        id=3,
        email='deneme',
    ), follow_redirects=True)
    assert "500" in rv.status


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


def test_add_annotation_with_put(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        body="http://thymesis.com/review/1",
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "200" in rv.status


def test_add_annotation_with_post(client):
    rv = client.post('/add/annotation/', data=dict(
        creator_id=1,
        body="http://thymesis.com/review/1",
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "405" in rv.status


def test_add_annotation_with_get(client):
    rv = client.get('/add/annotation/', data=dict(
        creator_id=1,
        body="http://thymesis.com/review/1",
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "405" in rv.status


def test_add_annotation_without_creator_id(client):
    rv = client.put('/add/annotation/', data=dict(
        body="http://thymesis.com/review/1",
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "200" in rv.status


def test_add_annotation_without_body(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "200" in rv.status


def test_add_annotation_without_target(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        body="http://thymesis.com/review/1"
    ), follow_redirects=True)
    assert "500" in rv.status


def test_add_annotation_with_custom_type(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body="http://thymesis.com/review/1",
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "200" in rv.status


def test_add_annotation_with_custom_context(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        context="https://www.w3.org/ns/anno.jsonld",
        type="Annotation",
        body="http://thymesis.com/review/1",
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "200" in rv.status


def test_add_annotation_with_body_dict(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "tagging", "type": "text",
              "selector": {"type": "TextPositionSelector", "start": 20, "end": 30}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "200" in rv.status


def test_add_annotation_with_body_dict_without_id(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"motivation": "tagging", "type": "text",
              "selector": {"type": "TextPositionSelector", "start": 20, "end": 30}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "500" in rv.status


def test_add_annotation_body_dict_with_invalid_motivation(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "putting", "type": "text",
              "selector": {"type": "TextPositionSelector", "start": 20, "end": 30}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "500" in rv.status


def test_add_annotation_body_dict_with_invalid_type(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "tagging", "type": "pdf",
              "selector": {"type": "TextPositionSelector", "start": 20, "end": 30}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "500" in rv.status


def test_add_annotation_body_dict_with_invalid_selector(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "tagging", "type": "text",
              "selector": {"type": "FragmentSelector", "start": 20, "end": 30}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "500" in rv.status


def test_add_annotation_body_dict_with_text_position_selector_without_start(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "tagging", "type": "text",
              "selector": {"type": "TextPositionSelector", "end": 30}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "500" in rv.status


def test_add_annotation_body_dict_with_text_position_selector_without_end(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "tagging", "type": "text",
              "selector": {"type": "TextPositionSelector", "start": 20}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "200" in rv.status


def test_add_annotation_body_dict_with_text_position_selector_with_string_start(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "tagging", "type": "text",
              "selector": {"type": "TextPositionSelector", "start": "20", "end": 30}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "200" in rv.status


def test_add_annotation_body_dict_with_text_position_selector_with_string_end(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "tagging", "type": "text",
              "selector": {"type": "TextPositionSelector", "start": 20, "end": "30"}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "200" in rv.status


def test_add_annotation_body_dict_with_text_position_selector_with_string_start_end(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "tagging", "type": "text",
              "selector": {"type": "TextPositionSelector", "start": "20", "end": "30"}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "200" in rv.status


def test_add_annotation_body_dict_with_url_string_body(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body="http://thymesis.com/review/1",
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "200" in rv.status


def test_add_annotation_body_dict_with_invalid_url_string_body(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body="review/1",
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "500" in rv.status


def test_add_annotation_with_target_dict(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "tagging", "type": "text",
              "selector": {"type": "TextPositionSelector", "start": 20, "end": 30}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "200" in rv.status


def test_add_annotation_with_target_dict_without_id(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "tagging", "type": "text",
              "selector": {"type": "TextPositionSelector", "start": 20, "end": 30}},
        target={"type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "500" in rv.status


def test_add_annotation_target_dict_with_invalid_motivation(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "tagging", "type": "text",
              "selector": {"type": "TextPositionSelector", "start": 20, "end": 30}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "motivation": "putting", "type": "Text",
                "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "500" in rv.status


def test_add_annotation_target_dict_with_invalid_type(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "tagging", "type": "text",
              "selector": {"type": "TextPositionSelector", "start": 20, "end": 30}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "pdf", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "500" in rv.status


def test_add_annotation_target_dict_with_invalid_selector(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "tagging", "type": "text",
              "selector": {"type": "TextPositionSelector", "start": 20, "end": 30}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "FragmentSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "500" in rv.status


def test_add_annotation_target_dict_with_text_position_selector_without_start(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "tagging", "type": "text",
              "selector": {"type": "TextPositionSelector", "start": 20, "end": 30}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "end": "795"}}
    ), follow_redirects=True)
    assert "500" in rv.status


def test_add_annotation_target_dict_with_text_position_selector_without_end(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "tagging", "type": "text",
              "selector": {"type": "TextPositionSelector", "start": 20, "end": 30}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412"}}
    ), follow_redirects=True)
    assert "200" in rv.status


def test_add_annotation_target_dict_with_text_position_selector_with_string_start(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "tagging", "type": "text",
              "selector": {"type": "TextPositionSelector", "start": "20", "end": 30}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": 795}}
    ), follow_redirects=True)
    assert "200" in rv.status


def test_add_annotation_target_dict_with_text_position_selector_with_string_end(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "tagging", "type": "text",
              "selector": {"type": "TextPositionSelector", "start": 20, "end": "30"}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": 412, "end": "795"}}
    ), follow_redirects=True)
    assert "200" in rv.status


def test_add_annotation_target_dict_with_text_position_selector_with_string_start_end(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body={"id": "http://thymesis.com/review/1", "motivation": "tagging", "type": "text",
              "selector": {"type": "TextPositionSelector", "start": "20", "end": "30"}},
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}
    ), follow_redirects=True)
    assert "200" in rv.status


def test_add_annotation_target_dict_with_url_string_target(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body="http://thymesis.com/review/1",
        target="http://thymesis.com/memory/1"
    ), follow_redirects=True)
    assert "200" in rv.status


def test_add_annotation_target_dict_with_invalid_url_string_target(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body="http://thymesis.com/review/1",
        target="memory/1",
    ), follow_redirects=True)
    assert "500" in rv.status


def test_add_annotation_target_dict_with_fragment_selector(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body="http://thymesis.com/review/1",
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "FragmentSelector", "conformsTo": "http://www.w3.org/TR/media-frags/",
                             "value": "xywh=10,20,30,50"}},
    ), follow_redirects=True)
    assert "200" in rv.status


def test_add_annotation_target_dict_fragment_selector_without_conformsto(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body="http://thymesis.com/review/1",
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "FragmentSelector", "value": "xywh=10,20,30,50"}},
    ), follow_redirects=True)
    assert "500" in rv.status


def test_add_annotation_target_dict_fragment_selector_without_value(client):
    rv = client.put('/add/annotation/', data=dict(
        creator_id=1,
        type="Annotation",
        body="http://thymesis.com/review/1",
        target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text", "source": "http://thymesis.com/memory/1",
                "selector": {"type": "FragmentSelector", "conformsTo": "http://www.w3.org/TR/media-frags/"}},
    ), follow_redirects=True)
    assert "500" in rv.status


def test_get_annotations_by_existing_creator(client):
    rv = client.get('/get/creator/1/annotations', follow_redirects=True)
    assert "200" in rv.status


def test_put_annotations_by_existing_creator(client):
    rv = client.put('/get/creator/1/annotations', follow_redirects=True)
    assert "405" in rv.status


def test_post_annotations_by_existing_creator(client):
    rv = client.put('/get/creator/1/annotations', follow_redirects=True)
    assert "405" in rv.status


def test_delete_annotations_by_existing_creator(client):
    rv = client.delete('/get/creator/1/annotations', follow_redirects=True)
    assert "405" in rv.status


def test_get_annotations_by_existing_creator_2(client):
    rv = client.get('/get/creator/2/annotations', follow_redirects=True)
    assert "200" in rv.status


def test_get_annotations_by_non_existing_creator(client):
    rv = client.get('/get/creator/200/annotations', follow_redirects=True)
    assert b"You are searching non-exist user annotations" in rv.data


def test_get_annotations_by_existing_creator_no_annotation(client):
    rv = client.get('/get/creator/3/annotations', follow_redirects=True)
    assert b"There is no annotation for the user" in rv.data


def test_delete_annotations_by_existing_id(client):
    rv = client.delete('/delete/annotation/1', follow_redirects=True)
    assert "200" in rv.data


def test_delete_annotations_by_non_existing_id(client):
    rv = client.delete('/delete/annotation/1000', follow_redirects=True)
    assert "200" in rv.data


def test_get_annotation_by_existing_id(client):
    rv = client.get('/get/annotation/1', follow_redirects=True)
    assert "200" in rv.data


def test_get_annotation_by_non_existing_id(client):
    rv = client.get('/get/annotation/100', follow_redirects=True)
    assert "500" in rv.data


def test_get_annotations_by_existing_ids(client):
    rv = client.get('/get/annotation/1234', follow_redirects=True)
    assert "200" in rv.data


def test_get_annotations_by_non_existing_ids(client):
    rv = client.get('/get/annotation/895', follow_redirects=True)
    assert "200" in rv.data


def test_get_annotations_by_two_decimal_ids(client):
    # when id is 89, it removes 8 and 9.
    # Issue opened but this endpoint is not used now.
    rv = client.get('/get/annotation/89', follow_redirects=True)
    assert "200" in rv.data


def test_get_annotations_by_target_id(client):
    rv = client.get('/get/annotation/target/a68b7e33-598d-4d7a-86f4-d94123bbc621', follow_redirects=True)
    assert "200" in rv.data


def test_get_annotations_by_target_non_exist_id(client):
    rv = client.get('/get/annotation/target/a68b7e33-598d', follow_redirects=True)
    assert "200" in rv.data
