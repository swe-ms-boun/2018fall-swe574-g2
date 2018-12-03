from django.db import models

# Create your models here.


class Users(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=70, unique=True)
    user_password = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)



class Posts(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    uri = models.CharField(max_length=45)
    title = models.CharField(max_length = 20)
    summary = models.CharField(max_length=30)
    post_body = models.CharField(max_length=3000)
    post_datetime = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField()



class Comments(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment_body = models.CharField(max_length = 200)
    Comments_datetime = models.DateTimeField(auto_now_add=True)





    
