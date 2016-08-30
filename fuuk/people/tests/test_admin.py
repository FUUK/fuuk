from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Permission, User
from django.core.urlresolvers import reverse
from django.forms import modelform_factory
from django.test import TestCase
from django.test.utils import override_settings

from fuuk.people.models import Agency, Course, Grant, GrantCollaborator, Human, Person
from ..admin import GrantAdmin


class MockRequest(object):
    pass


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


@override_settings(LANGUAGE_CODE='en')
class TestGrantAdmin(TestCase):
    """
    Test `GrantAdmin`.
    """
    def setUp(self):
        self.superusername = 'superuser'
        self.superpwd = 'superuser'
        self.username1 = 'user'
        self.pwd1 = 'user'
        self.username2 = 'user2'
        self.pwd2 = 'user2'
        self.request = MockRequest()
        self.site = AdminSite()
        self.superuser = User.objects.create_superuser(self.superusername, '', self.superpwd)
        self.user1 = User.objects.create_user(self.username1, '', self.pwd1)
        self.user1.is_staff = True
        self.user1.save()
        self.user2 = User.objects.create_user(self.username2, '', self.pwd2)
        self.user2.is_staff = True
        self.user2.user_permissions.add(Permission.objects.get(codename='change_grant'))
        self.user2.user_permissions.add(Permission.objects.get(codename='delete_grant'))
        self.user2.save()
        self.agency = Agency.objects.create(shortcut='TA', name='Test Agency')
        self.human1 = Human.objects.create(nickname='human1', user=self.user1)

    def test_index_view(self):
        self.request.user = self.user1
        admin = GrantAdmin(Grant, self.site)
        self.assertTrue(admin.has_module_permission(self.request))

    def test_add_view(self):
        self.request.user = self.user1
        admin = GrantAdmin(Grant, self.site)
        self.assertTrue(admin.has_add_permission(self.request))

    def test_editor_save(self):
        self.assertEqual(Grant.objects.count(), 0)
        self.request.user = self.user1
        admin = GrantAdmin(Grant, self.site)
        post_data = {'investigator_first_name': u'John',
                     'investigator_last_name': u'Smith',
                     'number': 1111,
                     'start': 2016,
                     'end': 2019,
                     'agency': self.agency.id,
                     'title_en': u'New Grant',
                     'annotation_en': u'New Grant annotation.',
                     }
        fields = [i for i in post_data.keys()]
        GrantForm = modelform_factory(Grant, fields=fields)
        grant_form = GrantForm(post_data)
        obj = grant_form.save(commit=False)
        admin.save_model(self.request, obj, grant_form, False)
        self.assertEqual(Grant.objects.count(), 1)
        self.assertEqual(Grant.objects.get(title_en=u'New Grant').editor, self.user1)

    def test_editor_save_change(self):
        self.request.user = self.user1
        admin = GrantAdmin(Grant, self.site)
        fields = ('investigator_first_name', 'investigator_last_name', 'number', 'start', 'end', 'agency', 'title_en',
                  'annotation_en',)
        grant = Grant.objects.create(investigator_first_name='John', investigator_last_name='Smith',
                                     number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        GrantForm = modelform_factory(Grant, fields=fields)
        grant_form = GrantForm(instance=grant)
        obj = grant_form.save(commit=False)
        admin.save_model(self.request, obj, grant_form, True)
        grant.refresh_from_db()
        self.assertEqual(grant.editor, None)

    def test_author_not_collaborator(self):
        self.assertEqual(Grant.objects.count(), 0)
        self.client.login(username=self.username1, password=self.pwd1)

        post_data = {'investigator_first_name': u'John',
                     'investigator_last_name': u'Smith',
                     'investigator_human': self.human1.id,
                     'number': 1,
                     'start': 2016,
                     'end': 2019,
                     'agency': self.agency.id,
                     'title_en': u'New Grant',
                     'annotation_en': u'New Grant annotation.',
                     'collaborators-TOTAL_FORMS': '1',
                     'collaborators-INITIAL_FORMS': '0',
                     'collaborators-MAX_NUM_FORMS': '',
                     'collaborators-0-first_name': u'John',
                     'collaborators-0-last_name': u'Smith',
                     'collaborators-0-human': self.human1.id,
                     }

        response = self.client.post(reverse('admin:people_grant_add'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Author can not be also collaborator.')

        human2 = Human.objects.create(nickname='human2', user=self.user2)
        post_data = {'investigator_first_name': u'John',
                     'investigator_last_name': u'Smith',
                     'investigator_human': self.human1.id,
                     'number': 1,
                     'start': 2016,
                     'end': 2019,
                     'agency': self.agency.id,
                     'title_en': u'New Grant',
                     'annotation_en': u'New Grant annotation.',
                     'collaborators-TOTAL_FORMS': '1',
                     'collaborators-INITIAL_FORMS': '0',
                     'collaborators-MAX_NUM_FORMS': '',
                     'collaborators-0-first_name': u'Jack',
                     'collaborators-0-last_name': u'Sparrow',
                     'collaborators-0-human': human2.id,
                     }

        response = self.client.post(reverse('admin:people_grant_add'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Grant.objects.count(), 1)

    def test_editor_change_permission(self):
        self.request.user = self.user1
        admin = GrantAdmin(Grant, self.site)
        self.assertTrue('editor' in admin.get_readonly_fields(self.request))

    def test_editor_change_permission_editor(self):
        self.request.user = self.user2
        admin = GrantAdmin(Grant, self.site)
        self.assertFalse('editor' in admin.get_readonly_fields(self.request))

    def test_editor_change_permission_superuser(self):
        self.request.user = self.superuser
        admin = GrantAdmin(Grant, self.site)
        self.assertFalse('editor' in admin.get_readonly_fields(self.request))

    def test_get_queryset_superuser(self):
        self.request.user = self.superuser
        admin = GrantAdmin(Grant, self.site)
        grant = Grant.objects.create(investigator_first_name='John', investigator_last_name='Smith',
                                     number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        self.assertTrue(grant in admin.get_queryset(self.request))

    def test_change_permission_superuser(self):
        self.request.user = self.superuser
        admin = GrantAdmin(Grant, self.site)
        grant = Grant.objects.create(investigator_first_name='John', investigator_last_name='Smith',
                                     number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        self.assertTrue(admin.has_change_permission(self.request, grant))

    def test_delete_permission_superuser(self):
        self.request.user = self.superuser
        admin = GrantAdmin(Grant, self.site)
        grant = Grant.objects.create(investigator_first_name='John', investigator_last_name='Smith',
                                     number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        self.assertTrue(admin.has_delete_permission(self.request, grant))

    def test_get_queryset_investigator_human(self):
        self.request.user = self.user1
        admin = GrantAdmin(Grant, self.site)
        grant = Grant.objects.create(investigator_first_name='John', investigator_last_name='User1',
                                     investigator_human=self.human1, number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        self.assertTrue(grant in admin.get_queryset(self.request))
        # test if `get_queryset` returns only unique grants.
        GrantCollaborator.objects.create(first_name='John', last_name='Collaborator1', grant=grant)
        GrantCollaborator.objects.create(first_name='Jack', last_name='Collaborator2', grant=grant)
        GrantCollaborator.objects.create(first_name='George', last_name='Collaborator3', grant=grant)
        self.assertEqual(admin.get_queryset(self.request).count(), 1)

    def test_change_permission_investigator_human(self):
        self.request.user = self.user1
        admin = GrantAdmin(Grant, self.site)
        grant = Grant.objects.create(investigator_first_name='John', investigator_last_name='User1',
                                     investigator_human=self.human1, number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        self.assertTrue(admin.has_change_permission(self.request, grant))

    def test_delete_permission_investigator_human(self):
        self.request.user = self.user1
        admin = GrantAdmin(Grant, self.site)
        grant = Grant.objects.create(investigator_first_name='John', investigator_last_name='User1',
                                     investigator_human=self.human1, number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        self.assertTrue(admin.has_delete_permission(self.request, grant))

    def test_get_queryset_change_permission(self):
        self.request.user = self.user2
        admin = GrantAdmin(Grant, self.site)
        grant = Grant.objects.create(investigator_first_name='John', investigator_last_name='Smith',
                                     number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        self.assertTrue(grant in admin.get_queryset(self.request))

    def test_change_permission_change_permission(self):
        self.request.user = self.user2
        admin = GrantAdmin(Grant, self.site)
        grant = Grant.objects.create(investigator_first_name='John', investigator_last_name='Smith',
                                     number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        self.assertTrue(admin.has_change_permission(self.request, grant))

    def test_delete_permission_delete_permission(self):
        self.request.user = self.user2
        admin = GrantAdmin(Grant, self.site)
        grant = Grant.objects.create(investigator_first_name='John', investigator_last_name='Smith',
                                     number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        self.assertTrue(admin.has_delete_permission(self.request, grant))

    def test_get_queryset_editor(self):
        self.request.user = self.user1
        admin = GrantAdmin(Grant, self.site)
        grant = Grant.objects.create(editor=self.user1, investigator_first_name='John', investigator_last_name='Smith',
                                     number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        self.assertTrue(grant in admin.get_queryset(self.request))

    def test_change_permission_editor(self):
        self.request.user = self.user1
        admin = GrantAdmin(Grant, self.site)
        grant = Grant.objects.create(editor=self.user1, investigator_first_name='John', investigator_last_name='Smith',
                                     number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        self.assertTrue(admin.has_change_permission(self.request, grant))

    def test_delete_permission_editor(self):
        self.request.user = self.user1
        admin = GrantAdmin(Grant, self.site)
        grant = Grant.objects.create(editor=self.user1, investigator_first_name='John', investigator_last_name='Smith',
                                     number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        self.assertTrue(admin.has_delete_permission(self.request, grant))

    def test_get_queryset_collaborator_human(self):
        self.request.user = self.user1
        admin = GrantAdmin(Grant, self.site)
        grant = Grant.objects.create(investigator_first_name='John', investigator_last_name='Smith',
                                     number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        GrantCollaborator.objects.create(first_name='Jack', last_name='User1', grant=grant, human=self.human1)
        self.assertTrue(grant in admin.get_queryset(self.request))

    def test_change_permission_collaborator_human(self):
        self.request.user = self.user1
        admin = GrantAdmin(Grant, self.site)
        grant = Grant.objects.create(investigator_first_name='John', investigator_last_name='Smith',
                                     number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        GrantCollaborator.objects.create(first_name='Jack', last_name='User1', grant=grant, human=self.human1)
        self.assertTrue(admin.has_change_permission(self.request, grant))

    def test_delete_permission_collaborator_human(self):
        self.request.user = self.user1
        admin = GrantAdmin(Grant, self.site)
        grant = Grant.objects.create(investigator_first_name='John', investigator_last_name='Smith',
                                     number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        GrantCollaborator.objects.create(first_name='Jack', last_name='User1', grant=grant, human=self.human1)
        self.assertTrue(admin.has_delete_permission(self.request, grant))

    def test_get_queryset_stranger(self):
        self.request.user = self.user1
        admin = GrantAdmin(Grant, self.site)
        grant = Grant.objects.create(investigator_first_name='John', investigator_last_name='Smith',
                                     number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        self.assertFalse(grant in admin.get_queryset(self.request))

    def test_change_permission_stranger(self):
        self.request.user = self.user1
        admin = GrantAdmin(Grant, self.site)
        grant = Grant.objects.create(investigator_first_name='John', investigator_last_name='Smith',
                                     number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        self.assertFalse(admin.has_change_permission(self.request, grant))

    def test_delete_permission_stranger(self):
        self.request.user = self.user1
        admin = GrantAdmin(Grant, self.site)
        grant = Grant.objects.create(investigator_first_name='John', investigator_last_name='Smith',
                                     number=1, start=2016, end=2019, agency=self.agency,
                                     title='Grant', annotation='About the Grant.')
        self.assertFalse(admin.has_delete_permission(self.request, grant))
