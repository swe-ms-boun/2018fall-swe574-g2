# coding=utf-8
from django.db import models


AGENT_CHOICES = (
    ("person", "Person"),
    ("organization", "Organization"),
    ("software", "Software"),
)


class User(models.Model):
    REQUIRED_FIELDS = ('email', 'type', 'home_page')

    nick = models.CharField(
        max_length=50,
        verbose_name=u'Kullanıcı Adı',
        db_index=True,
        unique=True
    )
    first_name = models.CharField(
        verbose_name=u'Ad',
        max_length=30,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        verbose_name=u'Soyad',
        max_length=30,
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name=u'Email Adresi',
        max_length=150,
        unique=True
    )

    type = models.CharField(max_length=30, choices=AGENT_CHOICES, default='person')
    home_page = models.CharField(max_length=100, unique=True)

    USERNAME_FIELD = 'nick'

    def __unicode__(self):
        return self.email

    def get_username(self):
        if self.username:
            return self.username
        return ''

    def get_email(self):
        if self.email:
            return self.email
        return ''

    def get_full_name(self):
        if self.first_name and self.last_name:
            return ' '.join([self.first_name, self.last_name])
        return ''

    def get_home_page(self):
        if self.home_page:
            return self.home_page
        return ''

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
