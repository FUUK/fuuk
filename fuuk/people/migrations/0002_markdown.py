# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import subprocess

from django.db import migrations, models
from django.utils.encoding import force_bytes, force_text

import fuuk.common.forms


def textile2markdown(text):
    """
    Use pandoc to convert textile to markdown.
    """
    r_pipe, w_pipe = os.pipe()
    os.write(w_pipe, force_bytes(text))
    os.close(w_pipe)
    result = subprocess.check_output(['pandoc', '-f', 'textile', '-t', 'markdown'], stdin=r_pipe)
    os.close(r_pipe)
    return force_text(result)


def convert_markup(apps, schema_editor):
    human_cls = apps.get_model('people', 'Human')
    grant_cls = apps.get_model('people', 'Grant')
    for human in human_cls.objects.all():
        human.interests_cs = textile2markdown(human.interests_cs)
        human.interests_en = textile2markdown(human.interests_en)
        human.stays_cs = textile2markdown(human.stays_cs)
        human.stays_en = textile2markdown(human.stays_en)
        human.cv_cs = textile2markdown(human.cv_cs)
        human.cv_en = textile2markdown(human.cv_en)
        human.save()

    for grant in grant_cls.objects.all():
        grant.annotation_cs = textile2markdown(grant.annotation_cs)
        grant.annotation_en = textile2markdown(grant.annotation_en)
        grant.save()


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_manytomany_null'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grant',
            name='annotation',
            field=models.TextField(help_text=fuuk.common.forms.get_markdown_help_text),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grant',
            name='annotation_cs',
            field=models.TextField(help_text=fuuk.common.forms.get_markdown_help_text, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='grant',
            name='annotation_en',
            field=models.TextField(help_text=fuuk.common.forms.get_markdown_help_text, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='human',
            name='cv',
            field=models.TextField(help_text=fuuk.common.forms.get_markdown_help_text, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='human',
            name='cv_cs',
            field=models.TextField(help_text=fuuk.common.forms.get_markdown_help_text, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='human',
            name='cv_en',
            field=models.TextField(help_text=fuuk.common.forms.get_markdown_help_text, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='human',
            name='interests',
            field=models.TextField(help_text=fuuk.common.forms.get_markdown_help_text, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='human',
            name='interests_cs',
            field=models.TextField(help_text=fuuk.common.forms.get_markdown_help_text, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='human',
            name='interests_en',
            field=models.TextField(help_text=fuuk.common.forms.get_markdown_help_text, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='human',
            name='stays',
            field=models.TextField(help_text=fuuk.common.forms.get_markdown_help_text, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='human',
            name='stays_cs',
            field=models.TextField(help_text=fuuk.common.forms.get_markdown_help_text, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='human',
            name='stays_en',
            field=models.TextField(help_text=fuuk.common.forms.get_markdown_help_text, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RunPython(convert_markup),
    ]
