# coding=utf-8
from django.db import models
import uuid


POST_TYPES = {
    'video': 'Video',
    'image': 'Image',
    'sound': 'Sound',
    'text': 'Text',
    'dataset': 'Dataset',
}


TARGET_TYPES = {
    'text': 'TextPositionSelector',
    'image': 'FragmentSelector'
}


class Users(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    username = models.CharField(max_length=50, null=True, blank=True)
    home_page = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=70, unique=True)
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    type = models.CharField(max_length=50, default="Person")

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_username(self):
        return self.username

    def get_home_page(self):
        return self.home_page

    def get_email(self):
        return self.email

    def __unicode__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Posts(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    uri = models.CharField(max_length=45)
    title = models.CharField(max_length=50)
    summary = models.CharField(max_length=100)
    body = models.CharField(max_length=3000)
    datetime = models.DateTimeField(auto_now_add=True)  #  Post creation date
    votes = models.IntegerField()
    location = models.CharField(max_length=200)
    date = models.DateField()  #  Post's content date
    type = models.CharField(max_length=20, choices=POST_TYPES)
    target_type = models.CharField(max_length=50, choices=TARGET_TYPES)
    #  If target type is text, start and end fields are required
    start = models.IntegerField()
    end = models.IntegerField()


class Comments(models.Model):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment_body = models.CharField(max_length=200)
    datetime = models.DateTimeField(auto_now_add=True)
