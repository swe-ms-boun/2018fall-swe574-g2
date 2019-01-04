from django.db import models
import uuid

POST_TYPES = (
    ('video', 'Video'),
    ('image', 'Image'),
    ('sound', 'Sound'),
    ('text', 'Text'),
    ('dataset', 'Dataset'),
)


TARGET_TYPES = (
    ('text', 'TextPositionSelector'),
    ('image', 'FragmentSelector'),
)


class Users(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    username = models.CharField(max_length=50, null=True, blank=True)
    home_page = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=70, unique=True)
    user_password = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    

class Posts(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    uri = models.CharField(max_length=45)
    title = models.CharField(max_length = 20)
    summary = models.CharField(max_length=30)
    body = models.CharField(max_length=3000)
    datetime = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField()
    location = models.CharField(max_length=200)
    image_url = models.CharField(max_length=300, null=True)
    happened_on = models.DateField(null=True)
    type = models.CharField(max_length=20, choices=POST_TYPES, null=True)
    target_type = models.CharField(max_length=50, choices=TARGET_TYPES, null=True)
    start = models.IntegerField(null=True)
    end = models.IntegerField(null=True)
    

class Comments(models.Model):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    body = models.CharField(max_length = 200)
    datetime = models.DateTimeField(auto_now_add=True)


