# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import fuuk.people.models.person
import fuuk.people.models.course
from django.conf import settings
import django.core.validators
import fuuk.people.models.thesis


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shortcut', models.CharField(max_length=10)),
                ('shortcut_en', models.CharField(max_length=10, null=True)),
                ('shortcut_cs', models.CharField(max_length=10, null=True)),
                ('name', models.CharField(max_length=100)),
                ('name_en', models.CharField(max_length=100, null=True)),
                ('name_cs', models.CharField(max_length=100, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=10, choices=[(b'BOOK', 'Book'), (b'ARTICLE', 'Article'), (b'TALK', 'Lecture'), (b'INVITED', 'Invited lecture'), (b'POSTER', 'Poster')])),
                ('identification', models.CharField(max_length=100, unique=True, null=True, blank=True)),
                ('year', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1979)])),
                ('title', models.CharField(max_length=300)),
                ('accepted', models.BooleanField(default=False, help_text='Mark this article as accepted only. No volume and pages has to be filled in.')),
                ('publication', models.CharField(max_length=100, null=True, blank=True)),
                ('volume', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(b'^[A-Z]?[0-9]{1,4}([-/][0-9]{1,4})?$')])),
                ('issue', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(b'^[A-Z]?[0-9]{1,4}([-/][0-9]{1,4})?$')])),
                ('page_from', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(b'^[A-Z]{0,2}[0-9]+(-[0-9]+)?$')])),
                ('article_number', models.BooleanField(default=False, help_text='Check if the journal is using article numbers instead of pages')),
                ('page_to', models.CharField(blank=True, max_length=10, null=True, help_text='Leave blank for one paged abstracts.', validators=[django.core.validators.RegexValidator(b'^[A-Z]{0,2}[0-9]+(-[0-9]+)?$')])),
                ('editors', models.CharField(max_length=200, null=True, blank=True)),
                ('publishers', models.CharField(max_length=200, null=True, blank=True)),
                ('place', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('file', models.FileField(max_length=200, upload_to=fuuk.people.models.course.attachment_filename)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.SmallIntegerField()),
                ('article', models.ForeignKey(to='people.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=10, validators=[django.core.validators.RegexValidator(b'^[A-Z]{2}([A-Z]{2}[0-9]{3}|[0-9]{3}[A-Z][0-9]{2}[A-Z]?)$')])),
                ('ls', models.CharField(blank=True, max_length=8, null=True, validators=[django.core.validators.RegexValidator(b'^[0-9]/[0-9] (Z|Zk|KZ|Zk/Z)$')])),
                ('zs', models.CharField(blank=True, max_length=8, null=True, validators=[django.core.validators.RegexValidator(b'^[0-9]/[0-9] (Z|Zk|KZ|Zk/Z)$')])),
                ('name', models.CharField(max_length=200)),
                ('name_en', models.CharField(max_length=200, null=True)),
                ('name_cs', models.CharField(max_length=200, null=True)),
                ('annotation', models.TextField(null=True, blank=True)),
                ('annotation_en', models.TextField(null=True, blank=True)),
                ('annotation_cs', models.TextField(null=True, blank=True)),
                ('note', models.TextField(null=True, blank=True)),
                ('note_en', models.TextField(null=True, blank=True)),
                ('note_cs', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('name_en', models.CharField(max_length=200, null=True)),
                ('name_cs', models.CharField(max_length=200, null=True)),
                ('fax', models.CharField(blank=True, max_length=20, unique=True, null=True, validators=[django.core.validators.RegexValidator(b'^\\+420( [0-9]{3}){3}$')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=20)),
                ('start', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1990), django.core.validators.MaxValueValidator(2018)])),
                ('end', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1990), django.core.validators.MaxValueValidator(2027)])),
                ('title', models.CharField(max_length=200)),
                ('title_en', models.CharField(max_length=200, null=True)),
                ('title_cs', models.CharField(max_length=200, null=True)),
                ('annotation', models.TextField()),
                ('annotation_en', models.TextField(null=True)),
                ('annotation_cs', models.TextField(null=True)),
                ('agency', models.ForeignKey(help_text='Contact administrators for different Grant Agency.', to='people.Agency')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Human',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(unique=True, max_length=20, validators=[django.core.validators.RegexValidator(b'^\\w+$')])),
                ('birth_date', models.DateField(null=True, blank=True)),
                ('birth_place', models.CharField(max_length=200, null=True, blank=True)),
                ('email', models.EmailField(max_length=200, unique=True, null=True, blank=True)),
                ('photo', models.ImageField(max_length=200, null=True, upload_to=fuuk.people.models.person.image_filename, blank=True)),
                ('display_posters', models.BooleanField(default=True, help_text='Uncheck to hide posters on your personal page.')),
                ('display_talks', models.BooleanField(default=True, help_text='Uncheck to hide talks not presented by you on your personal page.')),
                ('homepage', models.URLField(help_text=b'Fill in form of www.link.com/subpage', max_length=255, null=True, blank=True)),
                ('cv_file', models.FileField(max_length=200, upload_to=fuuk.people.models.person.cv_filename, blank=True)),
                ('subtitle', models.CharField(max_length=200, null=True, blank=True)),
                ('subtitle_en', models.CharField(max_length=200, null=True, blank=True)),
                ('subtitle_cs', models.CharField(max_length=200, null=True, blank=True)),
                ('cv', models.TextField(null=True, blank=True)),
                ('cv_en', models.TextField(null=True, blank=True)),
                ('cv_cs', models.TextField(null=True, blank=True)),
                ('interests', models.TextField(help_text='Use Textile (http://en.wikipedia.org/wiki/Textile_(markup_language)) and &amp;#8209; for endash.', null=True, blank=True)),
                ('interests_en', models.TextField(help_text='Use Textile (http://en.wikipedia.org/wiki/Textile_(markup_language)) and &amp;#8209; for endash.', null=True, blank=True)),
                ('interests_cs', models.TextField(help_text='Use Textile (http://en.wikipedia.org/wiki/Textile_(markup_language)) and &amp;#8209; for endash.', null=True, blank=True)),
                ('stays', models.TextField(null=True, blank=True)),
                ('stays_en', models.TextField(null=True, blank=True)),
                ('stays_cs', models.TextField(null=True, blank=True)),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('hyperlink', models.URLField(help_text=b'This hyperlink will be added to the news title. Fill in form of www.link.com', max_length=255, null=True, blank=True)),
                ('title', models.CharField(max_length=255)),
                ('title_en', models.CharField(max_length=255, null=True)),
                ('title_cs', models.CharField(max_length=255, null=True)),
                ('content', models.TextField()),
                ('content_en', models.TextField(null=True)),
                ('content_cs', models.TextField(null=True)),
            ],
            options={
                'verbose_name_plural': 'News',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('type', models.CharField(blank=True, max_length=10, null=True, choices=[(b'STAFF', 'Academic staff'), (b'OTHER', 'Other staff'), (b'PHD', 'PhD. student'), (b'MGR', 'Mgr. student'), (b'BC', 'Bc. student'), (b'GRAD', 'Graduate student'), (b'STUDENT', 'Student')])),
                ('prefix', models.CharField(max_length=20, null=True, blank=True)),
                ('first_name', models.CharField(help_text='Only first letter is required for article authors. In case of multiple first names, fill them separated by space.', max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('suffix', models.CharField(max_length=20, null=True, blank=True)),
                ('class_year', models.SmallIntegerField(null=True, blank=True)),
                ('advisor', models.ForeignKey(related_name='student', blank=True, to='people.Person', null=True)),
                ('human', models.ForeignKey(blank=True, to='people.Human', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('name_en', models.CharField(max_length=200, null=True)),
                ('name_cs', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, unique=True, null=True, validators=[django.core.validators.RegexValidator(b'^\\+420( [0-9]{3}){3}$')])),
                ('department', models.ForeignKey(blank=True, to='people.Department', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=5, choices=[(b'STUD', 'Student project'), (b'BC', 'Bachelor'), (b'MGR', 'Master'), (b'PHD', 'Doctoral'), (b'RNDR', 'Rigorous'), (b'PROF', 'Professor')])),
                ('year', models.SmallIntegerField(help_text='Year of thesis start or year of defence if already defended.', validators=[django.core.validators.MinValueValidator(1990)])),
                ('defended', models.BooleanField(default=False)),
                ('thesis_file', models.FileField(max_length=200, upload_to=fuuk.people.models.thesis.thesis_filename, blank=True)),
                ('title', models.CharField(max_length=200)),
                ('title_en', models.CharField(max_length=200, null=True)),
                ('title_cs', models.CharField(max_length=200, null=True)),
                ('annotation', models.TextField(null=True, blank=True)),
                ('annotation_en', models.TextField(null=True, blank=True)),
                ('annotation_cs', models.TextField(null=True, blank=True)),
                ('abstract', models.TextField(null=True, blank=True)),
                ('abstract_en', models.TextField(null=True, blank=True)),
                ('abstract_cs', models.TextField(null=True, blank=True)),
                ('keywords', models.CharField(max_length=200, null=True, blank=True)),
                ('keywords_en', models.CharField(max_length=200, null=True, blank=True)),
                ('keywords_cs', models.CharField(max_length=200, null=True, blank=True)),
                ('advisor', models.ForeignKey(related_name='thesis_lead', blank=True, to='people.Person', null=True)),
                ('author', models.ForeignKey(to='people.Person')),
                ('consultants', models.ManyToManyField(related_name='thesis_consulted', null=True, to='people.Person', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='person',
            name='place',
            field=models.ManyToManyField(help_text='Only used for grant (co-)applicants or staff.', to='people.Place', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='person',
            unique_together=set([('first_name', 'last_name', 'type')]),
        ),
        migrations.AddField(
            model_name='grant',
            name='author',
            field=models.ForeignKey(verbose_name='Applicant', to='people.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='grant',
            name='co_authors',
            field=models.ManyToManyField(related_name='grant_related', null=True, verbose_name='Co-applicant', to='people.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='grant',
            unique_together=set([('number', 'agency')]),
        ),
        migrations.AddField(
            model_name='course',
            name='lectors',
            field=models.ManyToManyField(to='people.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='practical_lectors',
            field=models.ManyToManyField(related_name='practical_course_set', null=True, to='people.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='author',
            name='person',
            field=models.ForeignKey(to='people.Person'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='author',
            unique_together=set([('article', 'order'), ('person', 'article')]),
        ),
        migrations.AddField(
            model_name='attachment',
            name='course',
            field=models.ForeignKey(to='people.Course'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='attachment',
            unique_together=set([('course', 'title')]),
        ),
        migrations.AddField(
            model_name='article',
            name='presenter',
            field=models.ForeignKey(blank=True, to='people.Person', help_text='Before selecting a presenter fill authors and press "Save and continue editing".', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='article',
            unique_together=set([('year', 'publication', 'volume', 'page_from', 'page_to')]),
        ),
        migrations.CreateModel(
            name='ArticleArticle',
            fields=[
            ],
            options={
                'verbose_name': 'Article',
                'proxy': True,
                'verbose_name_plural': 'Articles',
            },
            bases=('people.article',),
        ),
        migrations.CreateModel(
            name='ArticleBook',
            fields=[
            ],
            options={
                'verbose_name': 'Book',
                'proxy': True,
                'verbose_name_plural': 'Books',
            },
            bases=('people.article',),
        ),
        migrations.CreateModel(
            name='ArticleConference',
            fields=[
            ],
            options={
                'verbose_name': 'Conference paper',
                'proxy': True,
                'verbose_name_plural': 'Conference paper',
            },
            bases=('people.article',),
        ),
    ]
