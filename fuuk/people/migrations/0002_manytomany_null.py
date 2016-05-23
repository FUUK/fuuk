# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='practical_lectors',
            field=models.ManyToManyField(related_name=b'practical_course_set', to=b'people.Person', blank=True),
        ),
        migrations.AlterField(
            model_name='grant',
            name='co_authors',
            field=models.ManyToManyField(related_name=b'grant_related', verbose_name='Co-applicant', to=b'people.Person', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='place',
            field=models.ManyToManyField(help_text='Only used for grant (co-)applicants or staff.', to=b'people.Place', blank=True),
        ),
        migrations.AlterField(
            model_name='thesis',
            name='consultants',
            field=models.ManyToManyField(related_name=b'thesis_consulted', to=b'people.Person', blank=True),
        ),
    ]
