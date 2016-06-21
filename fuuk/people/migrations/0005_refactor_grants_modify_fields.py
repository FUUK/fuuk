# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0004_refactor_grants_data_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grant',
            name='author',
        ),
        migrations.RemoveField(
            model_name='grant',
            name='co_authors',
        ),
        migrations.AlterField(
            model_name='grant',
            name='investigator_first_name',
            field=models.CharField(max_length=50, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='grant',
            name='investigator_last_name',
            field=models.CharField(max_length=50, verbose_name='last name'),
        ),
    ]
