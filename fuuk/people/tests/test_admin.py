from django.contrib.auth.models import Permission, User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from fuuk.people.models import Course, Human, Person


@override_settings(LANGUAGE_CODE='en')
class TestHumanAdmin(TestCase):
    """
    Test `HumanAdmin`.
    """
    def setUp(self):
        self.user = User.objects.create(username='user', is_staff=True)
        self.user.set_password('user')
        self.user.save()

    def test_change_view(self):
        human = Human.objects.create(user=self.user)
        self.user.user_permissions.add(Permission.objects.get(codename='change_human'))
        self.client.login(username='user', password='user')

        response = self.client.get(reverse('admin:people_human_change', args=(human.pk, )))

        self.assertContains(response, 'Change human')


@override_settings(LANGUAGE_CODE='en')
class TestCourseAdmin(TestCase):
    """
    Test `CourseAdmin`.
    """
    def setUp(self):
        self.user = User.objects.create(username='user', is_staff=True)
        self.user.set_password('user')
        self.user.save()

    def test_change_view(self):
        human = Human.objects.create(user=self.user)
        person = Person.objects.create(human=human, first_name='Tester', last_name='Eda')
        self.user.user_permissions.add(Permission.objects.get(codename='change_course'))
        course = Course.objects.create(code='NOOE017', name_cs='Test course')
        course.lectors.add(person)
        course.save()
        self.client.login(username='user', password='user')

        response = self.client.get(reverse('admin:people_course_change', args=(course.pk, )))

        self.assertContains(response, 'Change course')
