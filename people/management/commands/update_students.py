from django.core.management.base import BaseCommand

from people.models import Person


class Command(BaseCommand):
    help = 'Updates class year of active students'

    def handle(self, *args, **options):
        verbosity = options['verbosity']
        for student in Person.objects.filter(type__in=('PHD', 'MGR', 'BC'), is_active=True):
            if verbosity >= 2:
                print 'Update class year of %s' % student

            student.class_year += 1
            student.save()
