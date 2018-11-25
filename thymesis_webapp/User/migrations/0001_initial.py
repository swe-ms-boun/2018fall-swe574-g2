# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nick', models.CharField(null=True, max_length=50, blank=True, unique=True, verbose_name='Kullan\u0131c\u0131 Ad\u0131', db_index=True)),
                ('first_name', models.CharField(max_length=30, null=True, verbose_name='Ad', blank=True)),
                ('last_name', models.CharField(max_length=30, null=True, verbose_name='Soyad', blank=True)),
                ('email', models.EmailField(unique=True, max_length=150, verbose_name='Email Adresi')),
                ('type', models.CharField(default=b'person', max_length=30, choices=[(b'person', b'Person'), (b'organization', b'Organization'), (b'software', b'Software')])),
                ('home_page', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
    ]
