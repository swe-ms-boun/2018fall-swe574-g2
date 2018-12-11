# -*- coding: utf-8 -*-
import datetime

from flask_wtf import FlaskForm
from wtforms import *

LANGUAGE_CHOICES = (
    ('tr', 'TR'),
    ('fr', 'FR'),
    ('en', 'EN')
)

CLASS_TYPES = (
    ('Video', 'Video'),
    ('Image', 'Image'),
    ('Sound', 'Sound'),
    ('Text', 'Text'),
    ('Dataset', 'Dataset'),
)

ANNOTATION_CLASS_TYPES = (
    ('Video', 'Video'),
    ('Image', 'Image'),
    ('Audio', 'Audio'),
    ('Text', 'Text'),
    ('Annotation', 'Annotation'),
    ('TextualBody', 'TextualBody')
)

CLASS_TYPE_FORMAT = (
    ('Image', 'image/jpeg'),
    ('Sound', 'audio/mpeg'),
    ('Sound', 'audio/mpeg'),
    ('Text', 'text/plain'),
    ('Textualbody', 'text/html')
)

TEXT_DIRECTION_CHOICES = (
    ("ltr", "ltr"),
    ("rtl", "rtl"),
    ("auto", "auto")
)

AGENT_CHOICES = (
    ("person", "Person"),
    ("organization", "Organization"),
    ("software", "Software"),
)

BODY_TARGET_CHOICES = (
    ("body", "Body"),
    ("target", "Target"),
)


class BaseForm(FlaskForm):
    class Meta:
        csrf = False


class BodyTarget(BaseForm):
    """
    Target and Body: https://www.w3.org/TR/annotation-model/#bodies-and-targets
        BODY_TARGET_CHOICES must be selected to create body or target.
        id: must have exactly 1 id with the value of the resource's IRI.
        format: The Body or Target should have exactly 1 format associated with it, but may have 0 or more.
        language: The Body or Target should have exactly 1 language associated with it, but may have 0 or more
        processingLanguage: Each Body and Target may have exactly 1 processingLanguage.
        textDirection: The Body or Target may have exactly 1 textDirection associated with it.
    """

    body_target_choice = SelectMultipleField('body_target_choice', choices=BODY_TARGET_CHOICES,
                                             validators=[validators.data_required()])
    id = StringField('id', validators=[validators.data_required()])
    format = SelectMultipleField('format', choices=CLASS_TYPE_FORMAT)
    language = SelectMultipleField('language', choices=LANGUAGE_CHOICES)
    type = SelectMultipleField('body_type', choices=CLASS_TYPES)
    text_direction = SelectMultipleField('text_direction', choices=TEXT_DIRECTION_CHOICES)
    processing_language = SelectMultipleField('processing_language', choices=LANGUAGE_CHOICES)

    def validate(self):
        """
            This method is used to validate required information are valid / provided or not.
        :return:
        """
        res = super(BaseForm, self).validate()
        body_target_choice = self.body_target_choice.data
        id = self.id.data

        if not (body_target_choice or id):
            raise ValueError("Body Target Choice and id fields at least one must be filled.")
        return res


class CreatorForm(BaseForm):
    """
        There should be exactly 1 creator relationship for Annotation and Body, but may be 0 or more than 1
        created_time: The time at which the resource was created.
            There should be exactly 1 created time property for Annotation and Body, and must not be more than 1.
        generator: The agent responsible for generating the serialization of the Annotation.
            There may be 0 or more generator relationships per Annotation
        generated: The time at which the Annotation serialization was generated.
            There may be exactly 1 generated property per Annotation, and must not be more than 1.
        modified: There may be exactly 1 modified property for Annotation and Body, and must not be more than 1.
        NOTE: The datetime must be a xsd:dateTime with the UTC timezone expressed as "Z".
    """
    id = StringField('id', validators=[validators.data_required()])
    type = SelectMultipleField('type', choices=AGENT_CHOICES, default="person")
    name = StringField('name')
    nick = StringField('nick')
    email = StringField('email', validators=[validators.data_required()])
    email_sha1 = StringField('email_sha1')
    home_page = StringField('home_page', validators=[validators.data_required()])

    def validate(self):
        """
            This method is used to validate required information are valid / provided or not.
        :return:
        """
        res = super(BaseForm, self).validate()
        id = self.id.data
        email = self.email.data
        home_page = self.home_page.data

        if not (email or id or home_page):
            raise ValueError("email_sha1, email, id or home_page fields at least one must be filled.")
        return res


class BaseAnnotation(BaseForm):
    """
    Base Annotation: https://www.w3.org/TR/annotation-model/#annotations
        context: The Annotation must have 1 or more @context values
        id: An Annotation must have exactly 1 IRI that identifies it.
        type: An Annotation must have 1 or more types, and the Annotation class must be one of them.
        body: There should be 1 or more body but may be 0.
        target: There must be 1 or more target relationships
    """
    context = StringField('context', default='https://www.w3.org/ns/anno.jsonld',
                          validators=[validators.data_required()])
    id = StringField('id', validators=[validators.data_required()])
    type = SelectMultipleField('type', default='Annotation', choices=ANNOTATION_CLASS_TYPES,
                               validators=[validators.data_required()])
    motivation = StringField('motivation')
    created_time = DateTimeField('created_time')
    body = StringField('body')
    target = StringField('target', validators=[validators.data_required()])
    creator_id = StringField('creator_id')

    def validate(self):
        """
            This method is used to validate required information are valid / provided or not.
        :return:
        """
        res = super(BaseForm, self).validate()

        context = self.context.data
        id = self.id.data
        target = self.target.data
        type = self.type.data

        if not (context or id or type or target):
            raise ValueError("context, id, type and target fields must be filled.")
        return res
