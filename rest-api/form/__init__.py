from flask_wtf import FlaskForm


class BaseForm(FlaskForm):
    class Meta:
        csrf = False


# TODO: This field is a basement (parent) class of annotations.
class Annotation(BaseForm):
    pass


class TextAnnotation(Annotation):
    pass


class ImageAnnotation(Annotation):
    pass


class SoundAnnotation(Annotation):
    pass


class Memory(BaseForm):
    pass


class Comment(BaseForm):
    pass


class Hashtag(BaseForm):
    pass
