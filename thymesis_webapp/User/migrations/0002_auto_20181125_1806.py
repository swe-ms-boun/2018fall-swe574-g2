# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='home_page',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='nick',
            field=models.CharField(unique=True, max_length=50, verbose_name='Kullan\u0131c\u0131 Ad\u0131', db_index=True),
        ),
    ]
