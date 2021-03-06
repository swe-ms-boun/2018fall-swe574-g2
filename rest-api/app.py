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
from config import *
from validate_email import validate_email

import logging

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

MONGO_URI = CONFIG.get('MONGO_URI')
USERNAME = CONFIG.get('USERNAME')
PASSWORD = CONFIG.get('PASSWORD')

app = Flask(__name__)

app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

REVIEW_BASE_URL = 'http://thymesis.com/review/'
ANNOTATION_BASE_URL = 'http://thymesis-api.herokuapp.com/annotation/'
MEMORY_BASE_URL = 'https://aqueous-wildwood-29737.herokuapp.com/memory/'

LOGGER = logging.getLogger()

AGENT_CHOICES = (
    ("person", "Person"),
    ("organization", "Organization"),
    ("software", "Software"),
)

CLASS_TYPES = {
    'video': 'Video',
    'image': 'Image',
    'sound': 'Sound',
    'text': 'Text',
    'dataset': 'Dataset',
    'textualbody': 'TextualBody'
}


MOTIVATION_TYPES = {
    'assessing': 'assessing',
    'bookmarking': 'bookmarking',
    'classifying': 'classifying',
    'commenting': 'commenting',
    'describing': 'describing',
    'editing': 'editing',
    'highlighting': 'highlighting',
    'identifying': 'identifying',
    'linking': 'linking',
    'moderating': 'moderating',
    'questioning': 'questioning',
    'replying': 'replying',
    'tagging': 'tagging'
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
#  @auth.login_required
@validate_form(form=CreatorForm)
def add_creator(form):
    """
        This endpoint is used to create a user.
        The email and home_page field should be unique for each user.
        email, id and home_page fields are required fields.
        name and nick fields are optional.
        Example put request:
            http://thymesis-api.herokuapp.com/add/creator?nick=memed&email=mehmet.kayaalp@boun.edu.tr&id=1&home_page=http://thymesis.com/memed
            http://thymesis-api.herokuapp.com/add/creator?email=mehmet.kayaalp@boun.edu.tr&id=1&home_page=http://thymesis.com/memed
    :param form:
    :return:
    """
    email = form.data['email']
    try:
        id = int(form.data['id'])
    except ValueError:
        return jsonify({'ok': False, 'message': 'The id shoule be an integer format.'}), 500

    is_valid = validate_email(email)
    if not is_valid:
        return jsonify({'ok': False, 'message': 'The email is not in a valid format.'}), 500

    is_email_exist = mongo.db.creator.find_one({"email": email})
    if is_email_exist:
        return jsonify({'ok': False, 'message': 'Ops, this email is already taken.'}), 500

    email_sha1 = hashlib.sha1(email).hexdigest()

    home_page = form.data['home_page']
    if not check_url_valid(home_page):
        return jsonify({'ok': False, 'message': 'The home page is not in URL format'}), 500

    mongo_query = {
        "email": form.data['email'],
        "id": form.data['id'],
        "email_sha1": email_sha1,
        "home_page": form.data['home_page'],
        #"created_time": datetime.datetime.now().isoformat() + "Z"
    }

    if 'name' in form.data and form.data['name']:
        mongo_query['name'] = form.data['name']

    if 'nick' in form.data and form.data['nick']:
        mongo_query['nick'] = form.data['nick']

    try:
        doc = mongo.db.creator.insert(mongo_query)
        return jsonify({'ok': True, 'message': 'Creator created successfully!'}), 200
    except Exception:
        return jsonify({'ok': False, 'message': 'Ops, creator could not be created! Talked with awesome team :)'}), 500


@app.route('/get/creator/<id>', methods=['GET'])
# @auth.login_required
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
        return jsonify({'ok': False, 'message': 'Ops, user not found!'}), 404


@app.route('/get/creator/list', methods=['GET'])
# @auth.login_required
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


@app.route('/update/creator', methods=['POST'])
#  @auth.login_required
@validate_form(form=UpdateCreatorForm)
def update_creator_info(form):
    """
        This endpoint is used to update or add a user's field.
        This field adds nick field to the user whose id = 3.
        In order to update a user field, id field is required.
        example call:
            http://thymesis-api.herokuapp.com/update/creator?nick=mehmet.kayaalp92&email=kagan@hotmail.com
            &id=3&home_page=http://thymesis.com/mk0730
    :param form:
    :return:
    """

    try:
        id = int(form.data['id'])
    except ValueError:
        return jsonify({'ok': False, 'message': 'The id shoule be an integer format.'}), 500

    user = mongo.db.creator.find_one({"id": id})
    mongo_query = {}

    email = form.data['email']

    name = form.data['name']
    nick = form.data['nick']
    home_page = form.data['home_page']

    if email:
        is_valid = validate_email(email)
        if not is_valid:
            return jsonify({'ok': False, 'message': 'The email is not valid.'}), 500
        mongo_query['email'] = email

    if name:
        mongo_query['name'] = name
    if nick:
        mongo_query['nick'] = nick
    if home_page:
        if check_url_valid(home_page):
            mongo_query['home_page'] = home_page
        else:
            return jsonify({'ok': False, 'message': 'The home page url is not valid.'}), 500

    if user:
        mongo.db.creator.update({'id': id}, {"$set": mongo_query}, upsert=True)
        return jsonify({'ok': True, 'message': 'User info are updated.'}), 200
    else:
        if email and home_page and id:
            mongo.db.creator.update({'id': id}, {"$set": mongo_query}, upsert=True)
            return jsonify(
                {'ok': False, 'message': 'Ops, user not found! We created the user with the given info'}), 200
        else:
            return jsonify(
                {'ok': False, 'message': 'Ops, user not found! First create the user'}), 404


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
            http://thymesis-api.herokuapp.com/add/annotation/?id=http://thymesis.com/annotation/1&creator_id=1&
            body: "http://example.org/review1"&target={"id": "a68b7e33-598d-4d7a-86f4-d94123bbc621", "type": "Text",
            source": "http://example.org/memory1", "selector": {"type": "TextPositionSelector", "start": "412", "end": "795"}}

        For annotation which target is directly id with selected image's xywh;
                https://www.w3.org/TR/annotation-model/#segments-of-external-resources the request can be:
                Look at example 4: IRIs with Fragment Components:
            http://thymesis-api.herokuapp.com/add/annotation/?id=http://thymesis.com/annotation/2&creator_id=1&
            body="http://example.org/description1"&target={"type": "Image", "format": "image/jpeg",
            "id": "http://example.com/image1%23xywh=100,100,300,300"}

            https://stackoverflow.com/a/23247395/5383769

        TODO: For an annotation which has FragmentSelector, the request'll be written.

    :param form:
    :return:
    """
    context = form.data['context']

    if not context:
        context = "https://www.w3.org/ns/anno.jsonld"

    #  context of the annotation should be like: https://www.w3.org/ns/anno.jsonld
    mongo_query = {
        "context": context,
        "created": datetime.datetime.now().isoformat() + "Z"
    }

    if 'type' in form.data['type']:
        #  If a user wants to add type, it is allowed to add type. However, only accepted field is Annotation.
        if "Annotation" in form.data['type']:
            mongo_query['type'] = form.data['type']
        else:
            return jsonify(
                {'ok': False, 'message': 'Type should be Annotation. Not something else.'}), 500
    else:
        #  It is required field and its default field is Annotation
        mongo_query['type'] = "Annotation"

    #  Body part is optional.
    if 'body' in form.data and form.data['body']:
        body_part = form.data['body']
        try:
            body_part = json.loads(body_part)
            mongo_query['body'] = {}
            try:
                mongo_query['body']['id'] = body_part['id']
            except KeyError:
                try:
                    mongo_query['body']['id'] = body_part['source']
                except KeyError:
                    pass

            if 'purpose' in body_part:
                # describing, tagging, assessing, bookmarking, classifying, commenting...
                motivation = body_part['purpose']
                try:
                    mongo_query['body']['purpose'] = MOTIVATION_TYPES[motivation]
                except KeyError:
                    return jsonify({'ok': False, 'message': 'Motivation is not valid'}), 500

            if 'motivation' in body_part:
                # describing, tagging, assessing, bookmarking, classifying, commenting...
                motivation = body_part['motivation']
                try:
                    mongo_query['body']['motivation'] = MOTIVATION_TYPES[motivation]
                except KeyError:
                    return jsonify({'ok': False, 'message': 'Motivation is not valid'}), 500

            if 'format' in body_part:
                mongo_query['body']['format'] = body_part['format']
            if 'language' in body_part:
                mongo_query['body']['language'] = body_part['language']

            #  type of the model are certain. There are only specific options listed below.
            #  If the type is not one of them, since it is not a required field, log it and pass it.
            if 'type' in body_part:
                type = body_part['type'].lower()
                try:
                    mongo_query['body']['type'] = CLASS_TYPES[type]
                except KeyError:
                    return jsonify({'ok': False, 'message': 'Class type is not valid'}), 500

            if 'text_direction' in body_part:
                mongo_query['body']['text_direction'] = body_part['text_direction']
            if 'processing_language' in body_part:
                mongo_query['body']['processing_language'] = body_part['processing_language']
            if 'id' in body_part:
                mongo_query['body']['id'] = body_part['id']
            if 'value' in body_part:
                mongo_query['body']['value'] = body_part['value']
            if 'creator' in body_part:
                mongo_query['body']['creator'] = body_part['creator']

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
                                return jsonify({'ok': False,
                                                'message': 'Start and end should number.'}), 500
                        else:
                            return jsonify({'ok': False,
                                            'message': 'For TextPosition type selector, '
                                                       'start and end field should be exist.'}), 500
                    elif 'FragmentSelector' in selector_part['type']:
                        mongo_query['body']['selector']['type'] = 'FragmentSelector'
                        if 'conformsTo' in selector_part and "value" in selector_part:
                            # http://www.w3.org/TR/media-frags/
                            mongo_query['body']['selector']['conformsTo'] = selector_part["conformsTo"]
                            # xywh=50,50,640,480
                            mongo_query['body']['selector']['value'] = selector_part["value"]
                        else:
                            return jsonify({'ok': False,
                                            'message': 'For FragmentSelector, '
                                                       'conformsTo and value field should be exist.'}), 500
                else:
                    return jsonify({'ok': False,
                                    'message': 'The type is missing for selector part. Selector part accepts either '
                                               'TextPositionSelector and FragmentSelector.'}), 500
        except ValueError:
            if '{' not in body_part:
                #  Body part can be directly a string like body: http://example.org/review1
                if check_url_valid(body_part):
                    mongo_query['body'] = body_part
                else:
                    return jsonify({'ok': False, 'message': 'Body url is not valid.'}), 500
            else:
                return jsonify({'ok': False, 'message': 'For body part the json format is not valid.'}), 500
        except Exception as e:
            return jsonify({'ok': False, 'message': e.message}), 500

    #  Target is a required field so there is no option to not have a target field.
    if 'target' in form.data and form.data['target']:
        body_part = form.data['target']
        try:
            body_part = json.loads(body_part)
            mongo_query['target'] = {}
            try:
                target_id = body_part['id']
                if not check_url_valid(target_id):
                    target_id = MEMORY_BASE_URL + target_id
                mongo_query['target']['id'] = str(target_id)
            except KeyError:
                try:
                    mongo_query['target']['id'] = body_part['source']
                except KeyError:
                    return jsonify(
                        {'ok': False, 'message': 'If you create a target, you should send id'}), 500

            if 'format' in body_part:
                mongo_query['target']['format'] = body_part['format']
            if 'language' in body_part:
                mongo_query['target']['language'] = body_part['language']

            #  type of the model are certain. There are only specific options listed below.
            #  If the type is not one of them, since it is not a required field, log it and pass it.
            if 'type' in body_part:
                type = body_part['type'].lower()
                try:
                    mongo_query['target']['type'] = CLASS_TYPES[type]
                except KeyError:
                    return jsonify({'ok': False, 'message': 'Class type is not valid'}), 500

            if 'text_direction' in body_part:
                mongo_query['target']['text_direction'] = body_part['text_direction']
            if 'processing_language' in body_part:
                mongo_query['target']['processing_language'] = body_part['processing_language']

            if 'purpose' in body_part:
                # describing, tagging, assessing, bookmarking, classifying, commenting...
                motivation = body_part['purpose']
                try:
                    mongo_query['target']['purpose'] = MOTIVATION_TYPES[motivation]
                except KeyError:
                    return jsonify({'ok': False, 'message': 'Purpose is not valid'}), 500

            if 'motivation' in body_part:
                # describing, tagging, assessing, bookmarking, classifying, commenting...
                motivation = body_part['motivation']
                try:
                    mongo_query['target']['motivation'] = MOTIVATION_TYPES[motivation]
                except KeyError:
                    return jsonify({'ok': False, 'message': 'Motivation is not valid'}), 500

            if 'selector' in body_part:
                mongo_query['target']['selector'] = {}
                selector_part = body_part['selector']
                #  Type is required for a selector.
                if "type" in selector_part:
                    if 'TextPositionSelector' in selector_part['type']:
                        mongo_query['target']['selector']['type'] = "TextPositionSelector"
                        # Check start and end exists.
                        # If type is TextPositionSelector, start and end fields are required.
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
                    elif 'FragmentSelector' in selector_part['type']:
                        mongo_query['target']['selector']['type'] = 'FragmentSelector'
                        if 'conformsTo' in selector_part and "value" in selector_part:
                            # http://www.w3.org/TR/media-frags/
                            mongo_query['target']['selector']['conformsTo'] = selector_part["conformsTo"]
                            # xywh=50,50,640,480
                            mongo_query['target']['selector']['value'] = selector_part["value"]
                else:
                    return jsonify({'ok': False,
                                    'message': 'The type is missing for selector part. Selector part accepts either '
                                               'TextPositionSelector and FragmentSelector.'}), 500
        except ValueError:
            if '{' not in body_part:
                #  Target part can be directly a string.
                if check_url_valid(body_part):
                    mongo_query['target'] = body_part
                else:
                    return jsonify({'ok': False, 'message': 'Target url is not valid.'}), 500
            else:
                return jsonify({'ok': False, 'message': 'For target part the json format is not valid.'}), 500
        except Exception as e:
            return jsonify({'ok': False, 'message': e.message}), 500

    # because only logged in users can be create annotation.
    #  So actually there should be a creator_id for our case although it is not required in annotation model.
    if 'creator_id' in form.data and form.data['creator_id']:
        user = mongo.db.creator.find_one({"id": form.data['creator_id']})
        if len(user) == 0:
            return jsonify(
                {'ok': False,
                 'message': 'The user does not exist. Please check user id: ' + form.data['creator_id']}), 404

        mongo_query["creator"] = {}

        #  Check and write necessary fields of the user.
        #  These fields have to already have for a user.
        check_user_field(mongo_query, user, 'id')
        check_user_field(mongo_query, user, 'email')
        check_user_field(mongo_query, user, 'email_sha1')
        check_user_field(mongo_query, user, 'home_page')
        #check_user_field(mongo_query, user, 'created_time')

        #  Check optional fields whether exists or not and if so write them.
        if 'type' in user:
            mongo_query["creator"]["type"] = user['type']
        else:
            #  By default, type is "Person" in the application.
            mongo_query["creator"]["type"] = 'Person'

        if 'name' in user:
            mongo_query['creator']['name'] = user['name']
        if 'nick' in user:
            mongo_query['creator']['nick'] = user['nick']
    #  creator is not required for an annotation.
    elif 'creator' in form.data and form.data['creator']:
        #  This part will not be used in our application.
        mongo_query['creator'] = {}
        creator_part = form.data['creator']
        if 'id' in creator_part:
            mongo_query['creator']['id'] = creator_part['id']
        else:
            return jsonify({'ok': True, 'message': 'Agent type should have an id'}), 500

        if 'type' in creator_part:
            try:
                mongo_query['creator']['type'] = AGENT_CHOICES[creator_part['type'].lower()]
            except KeyError:
                return jsonify({'ok': True, 'message': 'Agent type should be software, person or an organization'}), 500
            except AttributeError:
                return jsonify({'ok': True, 'message': 'Agent type should be string'}), 500
        else:
            return jsonify({'ok': True, 'message': 'Agent type should have a type'}), 500

        if 'name' in creator_part:
            mongo_query['creator']['name'] = creator_part['name']

        if 'nickname' in creator_part:
            mongo_query['creator']['nickname'] = creator_part['nickname']

        if 'email' in creator_part:
            mongo_query['creator']['email'] = creator_part['email']
        else:
            return jsonify({'ok': True, 'message': 'Agent type should have an email'}), 500

        if 'homepage' in creator_part:
            mongo_query['creator']['homepage'] = creator_part['homepage']
        else:
            return jsonify({'ok': True, 'message': 'Agent should have a homepage'}), 500

    if 'id' in form.data and form.data['id'] != "":
        mongo_query['id'] = form.data['id']
    elif 'target' in form.data and ('id' in body_part or 'source' in body_part):
        if 'id' in body_part and '#' in body_part['id']:
            splitted_body = body_part['id'].split('#')[0]
            annotation_number = mongo.db.annotation.count({'target.id': {'$regex': splitted_body}})
        else:
            if 'id' in body_part:
                annotation_number = mongo.db.annotation.count({'target.id': {'$regex': body_part['id']}})
            elif 'source' in body_part:
                annotation_number = mongo.db.annotation.count({'target.id': {'$regex': body_part['source']}})
        annotation_number += 1
        annotation_uri = ANNOTATION_BASE_URL + str(annotation_number)
        mongo_query['id'] = annotation_uri

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
            return jsonify({'ok': True, 'message': 'There is no annotation for the user'}), 404
        else:
            return jsonify({'ok': False, 'message': 'You are searching non-exist user annotations'}), 404


@app.route('/delete/annotation/<id>', methods=['DELETE'])
# @auth.login_required
def delete_specific_annotation(id):
    """
        This endpoint enables us to delete a specified annotation by given id.
        example request: http://thymesis-api.herokuapp.com/delete/annotation/1
    :param id:
    :return:
    """
    annotation_id = ANNOTATION_BASE_URL + id
    annotation = mongo.db.annotation.delete_one({"id": annotation_id})
    return jsonify({'ok': True, 'message': "Annotation is deleted if it exists"}), 200


@app.route('/annotation/<id>', methods=['GET'])
# @auth.login_required
def get_annotation(id):
    """
        This endpoint returns an annotation by given id.
        example call: http://thymesis-api.herokuapp.com/get/annotation/1
    :param id:
    :return:
    """
    annotation_id = ANNOTATION_BASE_URL + id
    annotation = mongo.db.annotation.find_one({"id": annotation_id})
    if annotation:
        #  ObjectID is not JSON serializable, so pop it.
        annotation.pop('_id')
        return jsonify({'ok': True, 'message': annotation}), 200
    else:
        return jsonify({'ok': False, 'message': "There is no annotation with this id: " + annotation_id}), 500


@app.route('/get/annotation/<id>', methods=['GET'])
# @auth.login_required
def get_annotation_by_id(id):
    """
        This endpoint returns an annotation by given id.
        example call: http://thymesis-api.herokuapp.com/get/annotation/1
    :param id:
    :return:
    """
    annotation_id = ANNOTATION_BASE_URL + id
    annotation = mongo.db.annotation.find_one({"id": annotation_id})
    if annotation:
        #  ObjectID is not JSON serializable, so pop it.
        annotation.pop('_id')
        return jsonify({'ok': True, 'message': annotation}), 200
    else:
        return jsonify({'ok': False, 'message': "There is no annotation with this id: " + annotation_id}), 500


@app.route('/get/annotations/<ids>', methods=['GET'])
# @auth.login_required
def get_annotation_by_ids(ids):
    """
        This endpoint is written to get multiple annotations of different ids.
        This endpoint should be used when calling a memory's annotations.
        example call: http://thymesis-api.herokuapp.com/get/annotations/1278
        1278 -> is the ids. ID 1, ID 2, ID 7 and ID 8.
        When a memory has 4 different annotations whose ids are 1,2,7 and 8, this endpoint should be called.
    :param ids:
    :return:
    """
    annotation_dict = dict()
    for id in ids:
        annotation_id = ANNOTATION_BASE_URL + id
        annotation = mongo.db.annotation.find_one({"id": annotation_id})
        if annotation:
            #  ObjectID is not JSON serializable, so pop it.
            annotation.pop('_id')
            annotation_dict[annotation['id']] = annotation
    return jsonify({'ok': True, 'message': annotation_dict}), 200


@app.route('/get/annotation/target/<id>', methods=['GET'])
# @auth.login_required
def get_annotation_by_target_id(id):
    """
        This endpoint is written to get annotations from a target id.
        This endpoint should be used when calling a memory's annotations.
        When calling memory whose id is 1, called below request to get its annotations
        example call: http://thymesis-api.herokuapp.com/get/annotation/target/a68b7e33-598d-4d7a-86f4-d94123bbc621
    :param id:
    :return:
    """
    if not check_url_valid(id):
        annotation_id = MEMORY_BASE_URL + id
    else:
        annotation_id = id

    annotation_list = mongo.db.annotation.find({'target.id': {'$regex': annotation_id}})
    annotations_list = list()
    for annotation in annotation_list:
        #  ObjectID is not JSON serializable, so pop it.
        annotation.pop('_id')
        annotations_list.append(annotation)
    return jsonify({'ok': True, 'message': annotations_list}), 200


@app.route('/add/review/', methods=['PUT'])
# @auth.login_required
@validate_form(form=ReviewCreationForm)
def add_review(form):
    body = form.data['body']

    review_counter = mongo.db.review.count({})
    review_counter = review_counter + 1
    if not body:
        body = ""

    mongo_query = {
        "body": body,
        "id": REVIEW_BASE_URL + str(review_counter)
    }

    mongo.db.review.insert(mongo_query)
    return jsonify({'ok': True, 'message': 'review id: ' + review_counter}), 200


@app.route('/get/review/<id>', methods=['GET'])
# @auth.login_required
def get_review(id):
    id = REVIEW_BASE_URL + str(id)
    review = mongo.db.review.find_one({"id": id})
    if review:
        review.pop('_id')
        return jsonify({'ok': True, 'message': review}), 200
    else:
        return jsonify({'ok': True, 'message': 'There is no review'}), 200


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
    app.run(debug=CONFIG.get('DEBUG'))
