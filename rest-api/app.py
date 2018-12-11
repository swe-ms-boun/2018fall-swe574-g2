#!flask/bin/python
# coding=utf-8
from flask import Flask, jsonify, make_response, abort, request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
from form import *
from flask_pymongo import PyMongo
from decorator import validate_form
import hashlib
import json

import logging

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/annotation"
mongo = PyMongo(app)

USERNAME = "root"
PASSWORD = "hoodyhu"

LOGGER = logging.getLogger()


@app.route('/')
def sitemap():
    links = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint in ['static', 'available_urls']:
            continue
        links.append('%s' % rule.rule)
    return jsonify(available_urls=sorted(links))


@app.route('/add/creator', methods=['PUT'])
# @auth.login_required
@validate_form(form=CreatorForm)
def add_creator(form):
    email = form.data['email']
    email_sha1 = hashlib.sha1(email).hexdigest()

    mongo_query = {
        "email": form.data['email'],
        "id": form.data['id'],
        "email_sha1": email_sha1,
        "home_page": form.data['home_page'],
        "created_time": datetime.datetime.now().isoformat()+"Z"
    }

    if 'name' in form.data and form.data['name']:
        mongo_query['name'] = form.data['name']

    if 'nick' in form.data and form.data['nick']:
        mongo_query['nick'] = form.data['nick']

    try:
        doc = mongo.db.creator.insert(mongo_query)
        return jsonify({'ok': True, 'message': 'Creator created successfully!'}), 200
    except Exception:
        return jsonify({'ok': False, 'message': 'Ops, creator could not be created! Talked with awesome team :)'}), 400


@app.route('/get/creator/<id>', methods=['GET'])
@auth.login_required
def get_specific_creator_by_id(id):
    user = mongo.db.creator.find_one({"id": id})
    if user:
        return jsonify({'ok': True, 'message': 'User email: ' + user['email']}), 200
    else:
        return jsonify({'ok': False, 'message': 'Ops, user not found!'}), 500


@app.route('/get/user/<username>', methods=['GET'])
@auth.login_required
def get_specific_creator_by_username(username):
    user = mongo.db.creator.find_one({"username": username})
    if user:
        return jsonify({'ok': True, 'message': 'User email: ' + user['email']}), 200
    else:
        return jsonify({'ok': False, 'message': 'Ops, user not found! Username is not necessary field'}), 404


@app.route('/add/annotation/', methods=['PUT'])
# @auth.login_required
@validate_form(form=BaseAnnotation)
def add_annotation(form):
    #  context of the annotation should be like: https://www.w3.org/ns/anno.jsonld
    mongo_query = {
        "context": form.data['context'],
        "id": form.data['id'],
        "type": form.data['type'],
        "created_time": datetime.datetime.now().isoformat()+"Z"
    }

    if 'body' in form.data and form.data['body']:
        body_part = form.data['body']
        body_part = json.loads(body_part)
        mongo_query['body'] = {}
        try:
            mongo_query['body']['id'] = body_part['id']
        except KeyError:
            jsonify(
                {'ok': False, 'message': 'If you create a body, you should send id'}), 400
            return

        if 'format' in body_part:
            mongo_query['body']['format'] = body_part['format']
        if 'language' in body_part:
            mongo_query['body']['language'] = body_part['language']
        if 'type' in body_part:
            mongo_query['body']['type'] = body_part['type']
        if 'text_direction' in body_part:
            mongo_query['body']['text_direction'] = body_part['text_direction']
        if 'processing_language' in body_part:
            mongo_query['body']['processing_language'] = body_part['processing_language']
        if 'selector' in body_part:
            mongo_query['body']['selector'] = {}
            selector_part = body_part['selector']
            if "id" in selector_part:
                mongo_query['body']['selector']['id'] = selector_part['id']
            if "type" in selector_part and "TextPositionSelector" in selector_part['type']:
                mongo_query['body']['selector']['type'] = selector_part['type']
                if "start" in selector_part:
                    mongo_query['body']['selector']['start'] = selector_part['start']
                if "end" in selector_part:
                    mongo_query['body']['selector']['end'] = selector_part['end']
            elif "type" in selector_part and "rectangle" in selector_part['type']:
                mongo_query['body']['selector']['type'] = selector_part['type']
                if "value" in selector_part:
                    # x,y,w,h;20,30,100,100
                    mongo_query['body']['selector']['value'] = selector_part['value']

    if 'target' in form.data and form.data['target']:
        body_part = form.data['target']
        body_part = json.loads(body_part)
        mongo_query['target'] = {}
        try:
            mongo_query['target']['id'] = body_part['id']
        except KeyError:
            jsonify(
                {'ok': False, 'message': 'If you create a target, you should send id'}), 400
            return

        if 'format' in body_part:
            mongo_query['target']['format'] = body_part['format']
        if 'language' in body_part:
            mongo_query['target']['language'] = body_part['language']
        if 'type' in body_part:
            mongo_query['target']['type'] = body_part['type']
        if 'text_direction' in body_part:
            mongo_query['target']['text_direction'] = body_part['text_direction']
        if 'processing_language' in body_part:
            mongo_query['target']['processing_language'] = body_part['processing_language']
        if 'selector' in body_part:
            mongo_query['target']['selector'] = {}
            selector_part = body_part['selector']
            if "id" in selector_part:
                mongo_query['target']['selector']['id'] = selector_part['id']
            if "type" in selector_part and "TextPositionSelector" in selector_part['type']:
                mongo_query['target']['selector']['type'] = selector_part['type']
                if "start" in selector_part:
                    mongo_query['target']['selector']['start'] = selector_part['start']
                if "end" in selector_part:
                    mongo_query['target']['selector']['end'] = selector_part['end']
            elif "type" in selector_part and "rectangle" in selector_part['type']:
                mongo_query['target']['selector']['type'] = selector_part['type']
                if "value" in selector_part:
                    # x,y,w,h;20,30,100,100
                    mongo_query['target']['selector']['value'] = selector_part['value']

    if 'creator_id' in form.data and form.data['creator_id']:
        user = mongo.db.creator.find_one({"id": form.data['creator_id']})
        if len(user) == 0:
            jsonify(
                {'ok': False, 'message': 'The user does not exist'}), 500
            return

        mongo_query["creator"] = {}

        check_user_field(mongo_query, user, 'id')

        if 'type' in user:
            mongo_query["creator"]["type"] = user['type']

        check_user_field(mongo_query, user, 'email')
        check_user_field(mongo_query, user, 'email_sha1')
        check_user_field(mongo_query, user, 'home_page')

        if 'created_date' in user:
            mongo_query["creator"]["created_date"] = user['created_date']
        else:
            mongo_query["creator"]["created_date"] = datetime.datetime.now().isoformat()+"Z"

        if 'name' in user:
            mongo_query['creator']['name'] = user['name']
        if 'nick' in user:
            mongo_query['creator']['nick'] = user['nick']

    try:
        doc = mongo.db.annotation.insert(mongo_query)
        return jsonify({'ok': True, 'message': 'Annotation is created successfully!'}), 200
    except Exception:
        return jsonify(
            {'ok': False, 'message': 'Ops, annotation could not be created! Talked with awesome team :)'}), 400


def check_user_field(mongo_query, user, field):
    try:
        mongo_query["creator"][field] = user[field]
    except KeyError:
        raise ('The creator does not have %s, please check it' % field)


@app.route('/get/creator/<creator_id>/annotations', methods=['GET'])
def get_annotations_by_creator(creator_id):
    annotations = mongo.db.annotation.find({"creator.id": creator_id})
    annotation_list = []
    for annotation in annotations:
        #  ObjectID is not JSON serializable so pop the _id.
        annotation.pop('_id')
        annotation_list.append(annotation)
    if annotations.count():
        return jsonify({'ok': True, 'message': annotation_list}), 200
    else:
        user = mongo.db.creator.find_one({"id": creator_id})
        if user:
            return jsonify({'ok': False, 'message': 'There is no annotation for the user'}), 500
        else:
            return jsonify({'ok': False, 'message': 'You are searching non-exist user annotations'}), 500


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@auth.get_password
def get_password(username):
    if username == USERNAME:
        return PASSWORD
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


if __name__ == '__main__':
    app.run(debug=True)
