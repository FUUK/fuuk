# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


mapping = {} # map places to institutions

def move_author_person_to_grant(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Grant = apps.get_model("people", "Grant")
    Institution = apps.get_model("people", "Institution")

    for grant in Grant.objects.all():
        grant.investigator_prefix = grant.author.prefix
        grant.investigator_first_name = grant.author.first_name
        grant.investigator_last_name = grant.author.last_name
        grant.investigator_suffix = grant.author.suffix
        grant.investigator_human = grant.author.human

        places = grant.author.place
        if places.exists() and not grant.author.type:
            without_department = places.filter(department__isnull=True)
            if without_department:
                place = without_department.order_by('id')[0]
            else:
                place = places.order_by('id')[0]
            if place.name in mapping:
                grant.investigator_institution = Institution.objects.get(name__exact=mapping[place.name]['name'])
            else:
                mapping[place.name] = {'name': place.name, 'name_cs': place.name_cs, 'name_en': place.name_en}
                institutions = Institution.objects.filter(name__exact=mapping[place.name]['name'])
                if not institutions:
                    institution = Institution(**mapping[place.name])
                    institution.save()
                    grant.investigator_institution = institution
                else:
                    grant.investigator_institution = institutions.first()

        grant.save()


def move_coauthors_to_collaborators(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Grant = apps.get_model("people", "Grant")
    GrantCollaborator = apps.get_model("people", "GrantCollaborator")
    Institution = apps.get_model("people", "Institution")

    for grant in Grant.objects.all():
        for person in grant.co_authors.all():
            collaborator = GrantCollaborator(
                grant=grant,
                prefix=person.prefix,
                first_name=person.first_name,
                last_name=person.last_name,
                suffix=person.suffix
            )
            collaborator.human = person.human

            places = person.place
            if places.exists() and not person.type:
                without_department = places.filter(department__isnull=True)
                if without_department:
                    place = without_department.order_by('id')[0]
                else:
                    place = places.order_by('id')[0]
                if place.name in mapping:
                    collaborator.institution = Institution.objects.get(name__exact=mapping[place.name]['name'])
                else:
                    mapping[place.name] = {'name': place.name, 'name_cs': place.name_cs, 'name_en': place.name_en}
                    institutions = Institution.objects.filter(name__exact=mapping[place.name]['name'])
                    if not institutions:
                        institution = Institution(**mapping[place.name])
                        institution.save()
                        collaborator.institution = institution
                    else:
                        collaborator.institution = institutions.first()

            collaborator.save()


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_refactor_grants'),
    ]

    operations = [
        migrations.RunPython(move_author_person_to_grant),
        migrations.RunPython(move_coauthors_to_collaborators),
    ]
