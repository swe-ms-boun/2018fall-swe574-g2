from django.db import models
import uuid

# Create your models here.


class Users(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    username = models.CharField(max_length=50, null=True, blank=True)
    home_page = models.CharField(max_length=100, null=True, blank=True)
    user_email = models.EmailField(max_length=70, unique=True)
    user_password = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    

class Posts(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    uri = models.CharField(max_length=45)
    title = models.CharField(max_length = 20)
    summary = models.CharField(max_length=30)
    post_body = models.CharField(max_length=3000)
    post_datetime = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField()
    location = models.CharField(max_length=200)
    

class Comments(models.Model):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment_body = models.CharField(max_length = 200)
    Comments_datetime = models.DateTimeField(auto_now_add=True)

