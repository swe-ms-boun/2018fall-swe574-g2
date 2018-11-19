# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import *


LANGUAGE_CHOICES = (
    ('tr', 'TR'),
    ('fr', 'FR'),
    ('en', 'EN')
)


CLASS_TYPES = (
    ('video', 'Video'),
    ('image', 'Image'),
    ('sound', 'Sound'),
    ('audio', 'Sound'),
    ('text', 'Text'),
    ('textualbody', 'TextualBody')
)


CLASS_TYPE_FORMAT = (
    # ('video', 'Video'),
    ('image', 'image/jpeg'),
    ('sound', 'audio/mpeg'),
    ('audio', 'audio/mpeg'),
    ('text', 'text/plain'),
    ('textualbody', 'text/html')
)


TEXT_DIRECTION_CHOICES = (
    ("ltr", "ltr"),
    ("rtl", "rtl")
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
    body_target_choice = SelectMultipleField('body_target_choice', choices=BODY_TARGET_CHOICES,
                                             validators=[validators.data_required()])
    id = StringField('id', validators=[validators.data_required()])
    format = SelectMultipleField('format', choices=CLASS_TYPE_FORMAT)
    language = SelectMultipleField('language', choices=LANGUAGE_CHOICES)
    type = SelectMultipleField('body_type', choices=CLASS_TYPES)
    text_direction = SelectMultipleField('text_direction', choices=TEXT_DIRECTION_CHOICES)
    processing_language = SelectMultipleField('processing_language', choices=LANGUAGE_CHOICES)

    def validate(self):
        res = super(BaseForm, self).validate()
        body_target_choice = self.body_target_choice.data
        id = self.id.data

        if not (body_target_choice or id):
            raise ValueError("Body Target Choice and id fields at least one must be filled.")
        return res


class CreatorForm(BaseForm):
    id = StringField('id', validators=[validators.data_required()])
    type = SelectMultipleField('type', choices=AGENT_CHOICES, default="person")
    name = StringField('name')
    nick = StringField('nick')
    email = StringField('email', validators=[validators.data_required()])
    email_sha1 = StringField('email_sha1')
    home_page = StringField('home_page', validators=[validators.data_required()])

    def validate(self):
        res = super(BaseForm, self).validate()
        id = self.id.data
        email = self.email.data
        home_page = self.home_page.data

        if not (email or id or home_page):
            raise ValueError("email_sha1 or email or id or home_page fields at least one must be filled.")
        return res


class BaseAnnotation(BaseForm):
    context = StringField('context', validators=[validators.data_required()])
    id = StringField('id', validators=[validators.data_required()])
    type = SelectMultipleField('type', choices=CLASS_TYPES, validators=[validators.data_required()])
    motivation = StringField('motivation')
    created_time = DateTimeField('created_time')
    body = StringField('body')
    target = StringField('target', validators=[validators.data_required()])
    creator_id = StringField('creator_id')

    def validate(self):
        res = super(BaseForm, self).validate()

        context = self.context.data
        id = self.id.data
        target = self.target.data
        type = self.type.data

        if not (context or id or type or target):
            raise ValueError("context and id and type and target fields at least one must be filled.")
        return res
