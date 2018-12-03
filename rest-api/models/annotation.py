from user import Creator


class Annotation(Creator):
    def __init__(self, *args, **kwargs):
        self.context = kwargs.get('context')
        self.id = kwargs.get('id')
        self.type = kwargs.get('type')
        self.motivation = kwargs.get('motivation')
        self.created_time = kwargs.get('created_time')
        self.body = kwargs.get('body')
        self.target = kwargs.get('target')
