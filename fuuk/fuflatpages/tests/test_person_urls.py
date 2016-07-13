from django.test import override_settings, TestCase

from fuuk.people.models import Human, Person


@override_settings(LANGUAGE_CODE='en')
class FlatpageViewTests(TestCase):
    def test_human_page_redirection(self):
        human = Human.objects.create(nickname="Human")
        Person.objects.create(human=human, is_active=True)

        response = self.client.get('/Human/')
        self.assertRedirects(response, '/people/person/Human/', status_code=301)

        response = self.client.get('/Human/papers/')
        self.assertRedirects(response, '/people/person/Human/papers/', status_code=301, target_status_code=404)

        response = self.client.get('/Unknown/papers/')
        self.assertContains(response, 'File not found', status_code=404)
