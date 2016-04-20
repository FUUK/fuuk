from django.contrib.auth.models import Permission, User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from fuuk.people.models import Human


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
