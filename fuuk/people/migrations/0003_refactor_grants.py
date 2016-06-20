# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import django.core.validators

import fuuk.common.forms


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('people', '0002_markdown'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('name_en', models.CharField(max_length=200, null=True, verbose_name='name')),
                ('name_cs', models.CharField(max_length=200, null=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'institution',
                'verbose_name_plural': 'institutions',
            },
        ),
        migrations.CreateModel(
            name='GrantCollaborator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('last_name', models.CharField(max_length=50, verbose_name='last name')),
                ('prefix', models.CharField(max_length=20, null=True, verbose_name='prefix', blank=True)),
                ('suffix', models.CharField(max_length=20, null=True, verbose_name='suffix',blank=True)),
                ('grant', models.ForeignKey(verbose_name='grant', related_name='collaborators', to='people.Grant')),
                ('human', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True,
                                            verbose_name='human', to='people.Human', null=True)),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True,
                                                  verbose_name='institution', to='people.Institution', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'co-applicant',
                'verbose_name_plural': 'co-applicants',
            },
        ),
        migrations.AlterUniqueTogether(
            name='grantcollaborator',
            unique_together=set([('human', 'grant')]),
        ),
        migrations.AlterModelOptions(
            name='grant',
            options={'verbose_name': 'grant', 'verbose_name_plural': 'grants'},
        ),
        migrations.AddField(
            model_name='grant',
            name='editor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='editor', blank=True,
                                    to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='grant',
            name='investigator_prefix',
            field=models.CharField(max_length=20, null=True, verbose_name='prefix', blank=True),
        ),
        migrations.AddField(
            model_name='grant',
            name='investigator_first_name',
            field=models.CharField(max_length=50, null=True, verbose_name='first_name', blank=True),
        ),
        migrations.AddField(
            model_name='grant',
            name='investigator_last_name',
            field=models.CharField(max_length=50, null=True, verbose_name='last_name', blank=True),
        ),
        migrations.AddField(
            model_name='grant',
            name='investigator_suffix',
            field=models.CharField(max_length=20, null=True, verbose_name='suffix', blank=True),
        ),
        migrations.AddField(
            model_name='grant',
            name='investigator_institution',
            field=models.ForeignKey(verbose_name='institution', blank=True, to='people.Institution', null=True),
        ),
        migrations.AddField(
            model_name='grant',
            name='investigator_human',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='human', blank=True,
                                    to='people.Human', null=True),
        ),
        migrations.AlterField(
            model_name='grant',
            name='number',
            field=models.CharField(max_length=20, verbose_name='grant number'),
        ),
        migrations.AlterField(
            model_name='grant',
            name='start',
            field=models.SmallIntegerField(verbose_name='start year',
                                           validators=[django.core.validators.MinValueValidator(1990),
                                           django.core.validators.MaxValueValidator(2017)]),
        ),
        migrations.AlterField(
            model_name='grant',
            name='end',
            field=models.SmallIntegerField(verbose_name='end year',
                                           validators=[django.core.validators.MinValueValidator(1990),
                                           django.core.validators.MaxValueValidator(2026)]),
        ),
        migrations.AlterField(
            model_name='grant',
            name='agency',
            field=models.ForeignKey(verbose_name='grant agency', to='people.Agency',
                                    help_text='Contact administrators for different Grant Agency.'),
        ),
        migrations.AlterField(
            model_name='grant',
            name='title',
            field=models.CharField(max_length=200, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='grant',
            name='title_cs',
            field=models.CharField(max_length=200, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='grant',
            name='title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='grant',
            name='annotation',
            field=models.TextField(help_text=fuuk.common.forms.get_markdown_help_text,
                                   verbose_name='grant annotation'),
        ),
        migrations.AlterField(
            model_name='grant',
            name='annotation_cs',
            field=models.TextField(help_text=fuuk.common.forms.get_markdown_help_text, null=True,
                                   verbose_name='grant annotation'),
        ),
        migrations.AlterField(
            model_name='grant',
            name='annotation_en',
            field=models.TextField(help_text=fuuk.common.forms.get_markdown_help_text, null=True,
                                   verbose_name='grant annotation'),
        ),
    ]
