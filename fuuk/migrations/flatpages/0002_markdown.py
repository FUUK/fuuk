# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import subprocess

from django.db import migrations
from django.utils.encoding import force_bytes, force_text


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
    flatpage_cls = apps.get_model('flatpages', 'FlatPage')
    for flatpage in flatpage_cls.objects.all():
        flatpage.content_cs = textile2markdown(flatpage.content_cs)
        flatpage.content_en = textile2markdown(flatpage.content_en)
        flatpage.save()


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(convert_markup),
    ]
