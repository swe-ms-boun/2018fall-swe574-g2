from flask import current_app


class Creator(object):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.id = kwargs.get('id')
        self.type = kwargs.get('type')
        self.nick = kwargs.get('nick')
        self.email = kwargs.get('email')
        self.email_sha1 = kwargs.get('email_sha1')
        self.home_page = kwargs.get('home_page')

