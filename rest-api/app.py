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
from utils import *

import logging

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://root:hoodyhu2@ds127624.mlab.com:27624/thymesis"
mongo = PyMongo(app)

USERNAME = "root"
PASSWORD = "hoodyhu2"

LOGGER = logging.getLogger()

CLASS_TYPES = {
    'video': 'Video',
    'image': 'Image',
    'sound': 'Sound',
    'text': 'Text',
    'dataset': 'Dataset',
}



@app.route('/')
def sitemap():
    """
        This is the base endpoint and lists the all endpoints that can be called by using this API.
    :return:
    """
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
    """
        This endpoint is used to create a user.
        The email and home_page field should be unique for each user.
        email, id and home_page fields are required fields.
        name and nick fields are optional.
        Example put request:
            http://thymesis-api.herokuapp.com/add/creator?nick=memed&email=mehmet.kayaalp@boun.edu.tr&id=1&home_page=thymesis.com/memed
            http://thymesis-api.herokuapp.com/add/creator?email=mehmet.kayaalp@boun.edu.tr&id=1&home_page=thymesis.com/memed
    :param form:
    :return:
    """
    email = form.data['email']

    is_email_exist = mongo.db.creator.find_one({"email": email})
    if is_email_exist:
        return jsonify({'ok': False, 'message': 'Ops, this email is already taken.'}), 500

    email_sha1 = hashlib.sha1(email).hexdigest()

    mongo_query = {
        "email": form.data['email'],
        "id": form.data['id'],
        "email_sha1": email_sha1,
        "home_page": form.data['home_page'],
        "created_time": datetime.datetime.now().isoformat() + "Z"
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
def get_spesific_creator_by_id(id):
    """
        This endpoint returns the information of the user by the given id.
            created_time: user creation time.
            email: user email.
            email_sha1: user email sha1 format.
            home_page: user home page on the thymesis page.
            id: user id.
        return:
        {
            "message": {
            "created_time": "2018-12-10T20:06:56.899177Z",
            "email": "mehmet.kayaalp@ozu.edu.tr",
            "email_sha1": "ce01e1d7c3593dedc0cb950cb557c71b96f99882",
            "home_page": "thymesis.com/memed",
            "id": "1"
            },
            "ok": true
        }
    :rtype: object
    """
    user = mongo.db.creator.find_one({"id": id})
    if user:
        #  _id type is an object so it is not possible to serialize it to JSON.
        #  Also this field is not important so pop it.
        user.pop('_id')
        return jsonify({'ok': True, 'message': user}), 200
    else:
        return jsonify({'ok': False, 'message': 'Ops, user not found!'}), 500


@app.route('/get/creator/list', methods=['GET'])
@auth.login_required
def get_all_creators_email():
    """
        this endpoint returns the list of all saved user's email addresses.
        format: 'user_id': 'user_email'
        returns:
            {
            "message": {
                "1": {
                    "created_time": "2018-12-10T20:06:56.899177Z",
                    "email": "mehmet.kayaalp@ozu.edu.tr",
                    "email_sha1": "ce01e1d7c3593dedc0cb950cb557c71b96f99882",
                    "home_page": "thymesis.com/memed",
                    "id": "1"
                },
                "2": {
                    "created_time": "2018-12-10T20:07:57.238812Z",
                    "email": "alan.endersoy@boun.edu.tr",
                    "email_sha1": "6100c275f4a7c2cb4a9a9644d5ebaee3122cf390",
                    "home_page": "thymesis.com/endersoy",
                    "id": "2"
                }
            },
            "ok": true
            }
    :rtype: object
    """
    user_list = mongo.db.creator.find({})
    user_email_dict = dict()
    for user in user_list:
        user.pop('_id')
        #  email and id is an mandatory field so it has to be for every user.
        user_email_dict[user['id']] = user
    return jsonify({'ok': True, 'message': user_email_dict}), 200


@app.route('/add/annotation/', methods=['PUT'])
# @auth.login_required
@validate_form(form=BaseAnnotation)
def add_annotation(form):
    """
        This endpoint is used to create an annotation.
        Context, id, type and created_time are required for this endpoint.
        However, context, created_time and type are filled automatically.
        user_id should be
        id should be a IRI like: http://example.org/anno24
        target is required.
        Body is optional but if there is a body, there has to be some required fields.
        There are two types of selectors supported which are either TextPositionSelector or FragmentSelector.
        TextPositionSelector selector should contains start and end numbers.

        For an annotation which has a TextPositionSelector, the request:
            http://thymesis-api.herokuapp.com/add/annotation/?id="http://thymesis.com/annotation/1"&creator_id=1
            &target={"type": "Text", "source": "http://example.org/memory1", "selector": {"type": "TextPositionSelector",
            "start": "412", "end": "795"}}

        TODO: For an annotation which has FragmentSelector, the request'll be written.

    :param form:
    :return:
    """
    #  context of the annotation should be like: https://www.w3.org/ns/anno.jsonld
    mongo_query = {
        "context": "https://www.w3.org/ns/anno.jsonld",
        "id": form.data['id'],
        "type": "Annotation",
        "created_time": datetime.datetime.now().isoformat() + "Z"
    }

    # Body part is optional.
    if 'body' in form.data and form.data['body']:
        body_part = form.data['body']
        body_part = json.loads(body_part)
        mongo_query['body'] = {}
        try:
            mongo_query['body']['id'] = body_part['id']
        except KeyError:
            try:
                mongo_query['body']['id'] = body_part['source']
            except KeyError:
                return jsonify(
                    {'ok': False, 'message': 'If you create a body, you should send id'}), 400

        if 'format' in body_part:
            mongo_query['body']['format'] = body_part['format']
        if 'language' in body_part:
            mongo_query['body']['language'] = body_part['language']

        # type of the model are certain. There are only specific options listed below.
        # If the type is not one of them, since it is not a required field, log it and pass it.
        if 'type' in body_part:
            type = body_part['type'].lower()
            try:
                mongo_query['body']['type'] = CLASS_TYPES[type]
            except KeyError:
                LOGGER.warning("Specified type is wrong. Check the type: " + type)

        if 'text_direction' in body_part:
            mongo_query['body']['text_direction'] = body_part['text_direction']
        if 'processing_language' in body_part:
            mongo_query['body']['processing_language'] = body_part['processing_language']
        if 'id' in body_part:
            mongo_query['target']['id'] = body_part['id']

        if 'selector' in body_part:
            mongo_query['body']['selector'] = {}
            selector_part = body_part['selector']
            #  Type is required for a selector.
            if "type" in selector_part:
                if 'TextPositionSelector' in selector_part['type']:
                    mongo_query['body']['selector']['type'] = 'TextPositionSelector'
                    if "start" in selector_part and 'end' in selector_part:
                        try:
                            #  Check start and end can be convertable to int or gave error.
                            start = int(selector_part['start'])
                            end = int(selector_part['end'])
                            mongo_query['body']['selector']['start'] = start
                            mongo_query['body']['selector']['end'] = end
                        except ValueError:
                            jsonify({'ok': False,
                                     'message': 'Start and end should number.'}), 500
                    else:
                        jsonify({'ok': False,
                                 'message': 'For TextPosition type selector, start and end field should be exist.'}), 500
            else:
                jsonify({'ok': False,
                         'message': 'The type is missing for selector part. Selector part accepts either '
                                    'TextPositionSelector and TextPositionSelector.'}), 500

    #  Target is a required field so there is no option to not have a target field.
    if 'target' in form.data and form.data['target']:
        body_part = form.data['target']
        body_part = json.loads(body_part)
        mongo_query['target'] = {}
        try:
            mongo_query['target']['id'] = body_part['id']
        except KeyError:
            try:
                mongo_query['target']['id'] = body_part['source']
            except KeyError:
                return jsonify(
                    {'ok': False, 'message': 'If you create a target, you should send id'}), 400

        if 'format' in body_part:
            mongo_query['target']['format'] = body_part['format']
        if 'language' in body_part:
            mongo_query['target']['language'] = body_part['language']

        # type of the model are certain. There are only specific options listed below.
        # If the type is not one of them, since it is not a required field, log it and pass it.
        if 'type' in body_part:
            type = body_part['type'].lower()
            try:
                mongo_query['target']['type'] = CLASS_TYPES[type]
            except KeyError:
                LOGGER.warning("Specified type is wrong. Check the type: " + type)

        if 'text_direction' in body_part:
            mongo_query['target']['text_direction'] = body_part['text_direction']
        if 'processing_language' in body_part:
            mongo_query['target']['processing_language'] = body_part['processing_language']
        if 'id' in body_part:
            mongo_query['target']['id'] = body_part['id']

        if 'selector' in body_part:
            mongo_query['target']['selector'] = {}
            selector_part = body_part['selector']
            #  Type is required for a selector.
            if "type" in selector_part:
                if 'TextPositionSelector' in selector_part['type']:
                    mongo_query['target']['selector']['type'] = "TextPositionSelector"
                    #  Check start and end exists. If type is TextPositionSelector, start and end fields are required.
                    if "start" in selector_part and 'end' in selector_part:
                        try:
                            #  Check start and end can be convertable to int or gave error.
                            start = int(selector_part['start'])
                            end = int(selector_part['end'])
                            mongo_query['target']['selector']['start'] = start
                            mongo_query['target']['selector']['end'] = end
                        except ValueError:
                            jsonify({'ok': False,
                                     'message': 'Start and end should number.'}), 500
                    else:
                        jsonify({'ok': False,
                                 'message': 'For TextPosition type selector, start and end field should be exist.'}), 500

            else:
                jsonify({'ok': False,
                         'message': 'The type is missing for selector part. Selector part accepts either '
                                    'TextPositionSelector and TextPositionSelector.'}), 500

    # creator id is not required field for anonymous users if exists.
    # DECISION: For our case, for now, anonymous user cannot be exist
    # because only logged in users can be create annotation.
    # So actually there should be a creator_id for our case although it is not required in annotation model.
    if 'creator_id' in form.data and form.data['creator_id']:
        user = mongo.db.creator.find_one({"id": form.data['creator_id']})
        print(user)
        if len(user) == 0:
            return jsonify(
                {'ok': False,
                 'message': 'The user does not exist. Please check user id: ' + form.data['creator_id']}), 500

        mongo_query["creator"] = {}

        #  Check and write necessary fields of the user.
        #  These fields have to already have for a user.
        check_user_field(mongo_query, user, 'id')
        check_user_field(mongo_query, user, 'email')
        check_user_field(mongo_query, user, 'email_sha1')
        check_user_field(mongo_query, user, 'home_page')
        check_user_field(mongo_query, user, 'created_time')

        #  Check optional fields whether exists or not and if so write them.
        if 'type' in user:
            mongo_query["creator"]["type"] = user['type']
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


@app.route('/get/creator/<creator_id>/annotations', methods=['GET'])
def get_annotations_by_creator(creator_id):
    """
     This endpoint returns a user's all saved annotations includes TextPositionSelector and FragmentSelector.
    :param creator_id:
    :return:
    """
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
