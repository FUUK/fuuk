# -*- coding: utf-8 -*-
"""
Unittests for views
"""
import datetime
import os

from django.core.files import File
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.translation import deactivate_all
from mock import Mock, patch

from fuuk.people.models import Agency, Article, Attachment, Author, Course, Grant, Human, Person, Thesis

_CLEANUPS = []


def setUpModule():
    patcher = override_settings(
        LANGUAGE_CODE='en',
        TEMPLATE_DIRS=(os.path.join(os.path.dirname(__file__), '../../templates/oppo'),
                       os.path.join(os.path.dirname(__file__), '../../templates')),
    )
    _CLEANUPS.append(patcher.disable)
    patcher.enable()

    deactivate_all()


def tearDownModule():
    for cleanup in reversed(_CLEANUPS):
        cleanup()


class TestArticleList(TestCase):
    def setUp(self):
        Article.objects.create(title='Perpetum mobile still running', type="ARTICLE", year="2013")
        Article.objects.create(title='White holes: Theory and observation', type="BOOK", year="2005")
        Article.objects.create(title='New type of black hole discovered', type="ARTICLE", year="2005")
        Article.objects.create(title='Report on a new warpdrive prototype', type="ARTICLE", year="2005")
        Article.objects.create(title='Some really old book on something we do not remember', type="BOOK", year="2003")
        # These shouldn't get counted
        Article.objects.create(title='Black hole types', type="POSTER", year="2002")
        Article.objects.create(title='Humble beginnings of the Warpdrives.', type="TALK", year="2001")
        Article.objects.create(title='Jumpgates are reality!', type="INVITED", year="2000")

    def test_basic(self):
        response = self.client.get('/people/articles/')
        self.assertContains(response, 'Year', count=1)
        self.assertEqual(response.context['year'], 2013)
        self.assertQuerysetEqual(response.context['years'], ['2013', '2005', '2003'])
        self.assertQuerysetEqual(response.context['object_list'], ['<Article: Perpetum mobile still running>'])

    def test_2005(self):
        response = self.client.get('/people/articles/2005/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['year'], 2005)
        self.assertQuerysetEqual(response.context['object_list'],
                                 ['<Article: New type of black hole discovered>',
                                  '<Article: Report on a new warpdrive prototype>',
                                  '<Article: White holes: Theory and observation>'])

    def test_1999(self):
        response = self.client.get('/people/articles/1999/')
        self.assertEqual(response.status_code, 404)


class TestGrantList(TestCase):
    def setUp(self):
        # This method is being overridden because GrantList uses date.today().year in get_queryset
        # Mock date.today().year
        date_mock = Mock()
        date_mock.today.return_value = datetime.date(2013, 1, 1)
        patcher = patch('fuuk.people.views.date', date_mock)
        self.addCleanup(patcher.stop)
        self.datetime_mock = patcher.start()

        # Prepare an author
        person = Person.objects.create(first_name="Test", last_name="Person")
        # Prepare agency
        agency = Agency.objects.create(name="GA")
        # Running
        Grant.objects.create(title='Perpetum mobile', start="1990", end="2014", number="1",
                             author=person, agency=agency)
        Grant.objects.create(title='White holes', start="2000", end="2013", number="2",
                             author=person, agency=agency)
        # Finished
        Grant.objects.create(title='Black holes', start="1990", end="2012", number="3", author=person,
                             agency=agency)
        Grant.objects.create(title='Warp drive', start="2000", end="2011", number="4", author=person,
                             agency=agency)
        # Too old to be included
        Grant.objects.create(title='Jumpgate', start="1990", end="2000", number="5", author=person, agency=agency)
        # Just started
        Grant.objects.create(title='Fancy new grant', start="2013", end="2020", number="6", author=person,
                             agency=agency)

    def test_basic(self):
        response = self.client.get('/people/grants/')
        self.assertContains(response, 'Current grants', count=1)
        self.assertContains(response, 'Ended grants', count=1)
        self.assertQuerysetEqual(response.context['object_list'],
                                 ['<Grant: Fancy new grant>', '<Grant: Perpetum mobile>', '<Grant: White holes>'])
        self.assertQuerysetEqual(response.context['grants_finished'],
                                 ['<Grant: Black holes>', '<Grant: Warp drive>'])


class TestGrantDetail(TestCase):
    def setUp(self):
        # Prepare an author
        person = Person.objects.create(first_name="Test", last_name="Person")
        # Prepare agency
        agency = Agency.objects.create(name="GA")
        # Prepare a grant with ids 1 and 2
        self.a = Grant.objects.create(start="2000", end="2001", agency=agency, number="1", author=person,
                                      title="Testing grant")
        self.b = Grant.objects.create(start="2001", end="2005", agency=agency, number="2", author=person,
                                      title="Second grant")

    def test_basic(self):
        response = self.client.get(('/people/grants/%s/' % self.a.id))
        self.assertContains(response, 'Testing grant', count=1)

    def test_second(self):
        response = self.client.get(('/people/grants/%s/' % self.b.id))
        self.assertContains(response, 'Second grant', count=1)

    def test_none(self):
        response = self.client.get('/people/grants/3000/')
        self.assertEqual(response.status_code, 404)


class TestThesesList(TestCase):
    def setUp(self):
        # Prepare an author
        person = Person.objects.create(first_name="Test", last_name="Person")
        Thesis.objects.create(title='Theoretical calculations of white holes', type='BC', year=2001, author=person,
                              defended=True)
        Thesis.objects.create(title='Jumpgates limitations', type='MGR', year=2002, author=person, defended=True)
        Thesis.objects.create(title='Wow I have finished my PhD really fast', type='PHD', year=2002, author=person,
                              defended=True)
        # Should not get counted
        Thesis.objects.create(title="Not so good", type='RNDR', year=2003, author=person)
        Thesis.objects.create(title="Professor's thesis", type='PROF', year=2004, author=person)

    def test_basic(self):
        response = self.client.get('/people/theses/')
        self.assertContains(response, 'By thesis type', count=1)
        self.assertQuerysetEqual(response.context['object_list'], [])
        self.assertEqual(len(response.context['types']), 3)
        self.assertQuerysetEqual(response.context['years'], ['2002', '2001'])

    def test_year(self):
        response = self.client.get('/people/theses/?year=2002')
        self.assertContains(response, 'Theses defended in year 2002', count=1)
        self.assertEqual(response.context['year'], '2002')
        self.assertQuerysetEqual(response.context['object_list'], ['<Thesis: Wow I have finished my PhD really fast>',
                                                                   '<Thesis: Jumpgates limitations>'])

    def test_type(self):
        response = self.client.get('/people/theses/?type=BC')
        self.assertEqual(response.context['type'], 'BC')
        self.assertContains(response, 'Defended bachelor theses', count=1)
        self.assertQuerysetEqual(response.context['object_list'], ['<Thesis: Theoretical calculations of white holes>'])


class TestThesisDetail(TestCase):
    def setUp(self):
        # Prepare an author
        human = Human.objects.create(nickname='Person_Test')
        person = Person.objects.create(first_name="Test", last_name="Person", human=human)
        self.a = Thesis.objects.create(type='BC', year=2000, author=person, title='Test thesis')
        self.b = Thesis.objects.create(type='BC', year=2000, author=person, title='Defended test thesis',
                                       defended=True)

    def test_basic(self):
        response = self.client.get(('/people/thesis/id=%s/' % self.a.id))
        self.assertContains(response, 'Test thesis', count=1)
        self.assertContains(response, 'Test Person', count=1)
        self.assertNotContains(response, 'Keywords')

    def test_defended(self):
        response = self.client.get(('/people/thesis/id=%s/' % self.b.id))
        self.assertContains(response, 'Defended test thesis', count=1)
        self.assertContains(response, 'Keywords', count=1)


class TestCourseList(TestCase):
    def setUp(self):
        Course.objects.create(name='Testing course', code='AA001')
        Course.objects.create(name='Second course', code='AA002')

    def test_basic(self):
        response = self.client.get('/people/courses/')
        self.assertContains(response, 'Testing course', count=1)
        self.assertQuerysetEqual(response.context['object_list'],
                                 ['<Course: Testing course>', '<Course: Second course>'], ordered=False)


class TestDownloadList(TestCase):
    def setUp(self):
        course = Course.objects.create(name='Course with attachment', code='AA001')
        Course.objects.create(name='Course without attachment', code='AA002')
        a_file = open(os.path.join(os.path.dirname(__file__), 'test_views.py'))
        Attachment.objects.create(course=course, title='The attachment', file=File(a_file))

    def test_basic(self):
        response = self.client.get('/people/downloads/')
        self.assertContains(response, 'Course with attachment', count=1)
        self.assertContains(response, 'The attachment', count=1)
        self.assertNotContains(response, 'Course without attachment')


class TestPeopleList(TestCase):
    def setUp(self):
        human = Human.objects.create(nickname='Bachelor_Test')
        Person.objects.create(type='BC', first_name='Test', last_name='Bachelor', human=human)
        human = Human.objects.create(nickname='Magister_Test')
        Person.objects.create(type='MGR', first_name='Test', last_name='Magister', human=human)
        human = Human.objects.create(nickname='Doctoral_Test')
        Person.objects.create(type='PHD', first_name='Test', last_name='Doctoral', human=human)
        human = Human.objects.create(nickname='Staff_Test')
        Person.objects.create(type='STAFF', first_name='Test', last_name='Staff', human=human)
        human = Human.objects.create(nickname='Other_Test')
        Person.objects.create(type='OTHER', first_name='Test', last_name='Other', human=human)
        human = Human.objects.create(nickname='Grad_Test')
        Person.objects.create(type='GRAD', first_name='Test', last_name='Graduate', human=human)
        human = Human.objects.create(nickname='Student_Test')
        Person.objects.create(type='STUDENT', first_name='Test', last_name='Student', human=human)
        human = Human.objects.create(nickname='Retired_Test')
        Person.objects.create(type='STAFF', first_name='Test', last_name='Retired', human=human,
                              is_active=False)
        human = Human.objects.create(nickname='Other_InactiveTest')
        Person.objects.create(type='OTHER', first_name='Test', last_name='Alsoretired', human=human,
                              is_active=False)
        # These shouldn't get included
        human = Human.objects.create(nickname='Bachelor_Inactive')
        Person.objects.create(type='BC', first_name='FalseTest', last_name='Bachelor', human=human,
                              is_active=False)
        human = Human.objects.create(nickname='Magister_Inactive')
        Person.objects.create(type='MGR', first_name='FalseTest', last_name='Magister', human=human,
                              is_active=False)
        human = Human.objects.create(nickname='Doctoral_Inactive')
        Person.objects.create(type='PHD', first_name='FalseTest', last_name='Doctoral', human=human,
                              is_active=False)
        human = Human.objects.create(nickname='Grad_Inactive')
        Person.objects.create(type='GRAD', first_name='FalseTest', last_name='Graduate', human=human,
                              is_active=False)
        human = Human.objects.create(nickname='Student_Inactive')
        Person.objects.create(type='STUDENT', first_name='FalseTest', last_name='Student', human=human,
                              is_active=False)

    def test_phd(self):
        response = self.client.get('/people/phd/')
        self.assertNotContains(response, 'Test Bachelor')
        self.assertNotContains(response, 'Test Magister')
        self.assertNotContains(response, 'Test Student')
        self.assertContains(response, 'Test Doctoral', count=1)
        self.assertNotContains(response, 'Test Staff')
        self.assertNotContains(response, 'Test Graduate')
        self.assertNotContains(response, 'Test Other')
        self.assertNotContains(response, 'Test Retired')
        self.assertNotContains(response, 'FalseTest')
        self.assertQuerysetEqual(response.context['object_list'], ['<Person: Doctoral Test (PhD. student)>'])
        self.assertEqual(response.context['title'], 'PhD. students')

    def test_staff(self):
        response = self.client.get('/people/staff/')
        self.assertNotContains(response, 'Test Bachelor')
        self.assertNotContains(response, 'Test Magister')
        self.assertNotContains(response, 'Test Student')
        self.assertNotContains(response, 'Test Doctoral')
        self.assertContains(response, 'Test Staff', count=1)
        self.assertNotContains(response, 'Test Graduate')
        self.assertNotContains(response, 'Test Other')
        self.assertNotContains(response, 'Test Retired')
        self.assertNotContains(response, 'FalseTest')
        self.assertQuerysetEqual(response.context['object_list'], ['<Person: Staff Test (Academic staff)>'])
        self.assertEqual(response.context['title'], 'Academic staff')

    def test_other(self):
        response = self.client.get('/people/other/')
        self.assertNotContains(response, 'Test Bachelor')
        self.assertNotContains(response, 'Test Magister')
        self.assertNotContains(response, 'Test Student')
        self.assertNotContains(response, 'Test Doctoral')
        self.assertNotContains(response, 'Test Staff')
        self.assertNotContains(response, 'Test Graduate')
        self.assertContains(response, 'Test Other', count=1)
        self.assertNotContains(response, 'Test Retired')
        self.assertQuerysetEqual(response.context['object_list'], ['<Person: Other Test (Other staff)>'])
        self.assertNotContains(response, 'FalseTest')
        self.assertEqual(response.context['title'], 'Other staff')

    def test_students(self):
        response = self.client.get('/people/students/')
        self.assertContains(response, 'Test Bachelor', count=1)
        self.assertQuerysetEqual(response.context['bachelors'], ['<Person: Bachelor Test (Bc. student)>'])
        self.assertContains(response, 'Test Magister', count=1)
        self.assertQuerysetEqual(response.context['object_list'], ['<Person: Magister Test (Mgr. student)>'])
        self.assertContains(response, 'Test Student', count=1)
        self.assertQuerysetEqual(response.context['students'], ['<Person: Student Test (Student)>'])
        self.assertNotContains(response, 'Test Doctoral')
        self.assertNotContains(response, 'Test Staff')
        self.assertNotContains(response, 'Test Graduate')
        self.assertNotContains(response, 'Test Other')
        self.assertNotContains(response, 'Test Retired')
        self.assertNotContains(response, 'FalseTest')

    def test_graduates(self):
        response = self.client.get('/people/graduates/')
        self.assertNotContains(response, 'Test Bachelor')
        self.assertNotContains(response, 'Test Magister')
        self.assertNotContains(response, 'Test Student')
        self.assertNotContains(response, 'Test Doctoral')
        self.assertNotContains(response, 'Test Staff')
        self.assertContains(response, 'Test Graduate', count=1)
        self.assertNotContains(response, 'Test Other')
        self.assertNotContains(response, 'Test Retired')
        self.assertQuerysetEqual(response.context['object_list'], ['<Person: Graduate Test (Graduate student)>'])
        self.assertNotContains(response, 'FalseTest')
        self.assertEqual(response.context['title'], 'Graduate students')

    def test_retired(self):
        response = self.client.get('/people/retired/')
        self.assertNotContains(response, 'Test Bachelor')
        self.assertNotContains(response, 'Test Magister')
        self.assertNotContains(response, 'Test Student')
        self.assertNotContains(response, 'Test Doctoral')
        self.assertNotContains(response, 'Test Staff')
        self.assertNotContains(response, 'Test Graduate')
        self.assertNotContains(response, 'Test Other')
        self.assertContains(response, 'Test Retired', count=1)
        self.assertContains(response, 'Test Alsoretired')
        self.assertQuerysetEqual(response.context['object_list'], ['<Person: Alsoretired Test (Other staff)>',
                                                                   '<Person: Retired Test (Academic staff)>'])
        self.assertNotContains(response, 'FalseTest')
        self.assertEqual(response.context['title'], 'Former members')


class TestPersonalPages(TestCase):
    def setUp(self):
        # Testing person
        H1 = Human.objects.create(nickname='Person_test')
        P1 = Person.objects.create(type='STAFF', first_name='Test', last_name='Person', human=H1)
        # Inactive version of previous
        Person.objects.create(type='PHD', first_name='Test', last_name='Person', human=H1, is_active=False)
        # False person
        H2 = Human.objects.create(nickname='False_person')
        P2 = Person.objects.create(type='SATFF', first_name='False', last_name='Person', human=H2)
        Thesis.objects.create(type='PHD', author=P1, title='Ongoing PHD', year=2000)
        Thesis.objects.create(type='MGR', author=P1, title='Finished MGR', year=2000,
                              defended=True)
        Thesis.objects.create(type='BC', author=P1, title='Finished BC', year=1997,
                              defended=True)
        # Articles
        A1 = Article.objects.create(type="ARTICLE", year="2013", title='First article')
        A2 = Article.objects.create(type="BOOK", year="2005", title='Newest trends in writing django tests')
        A3 = Article.objects.create(type="ARTICLE", year="2005", title='False article')
        A4 = Article.objects.create(type="ARTICLE", year="2005", title='It is hard to come up with some funny thing...')
        Article.objects.create(type="BOOK", year="2003", title='My first book')
        # Author join
        Author.objects.create(person=P1, article=A1, order=1)
        Author.objects.create(person=P1, article=A2, order=1)
        Author.objects.create(person=P1, article=A4, order=2)
        Author.objects.create(person=P2, article=A3, order=1)
        # Students
        H3 = Human.objects.create(nickname='Student_test')
        Person.objects.create(type='BC', first_name='Test', last_name='Student', human=H3,
                              advisor=P1)
        H4 = Human.objects.create(nickname='Student_false')
        Person.objects.create(type='BC', first_name='False', last_name='Student', human=H4,
                              advisor=P2)
        H5 = Human.objects.create(nickname='Student_finished')
        Person.objects.create(type='BC', first_name='Finished', last_name='Student', human=H5,
                              advisor=P1, is_active=False)
        # Courses
        Course.objects.create(name='Testing course', code='AA001').lectors.add(P1)
        Course.objects.create(name='False course', code='FF001').lectors.add(P2)
        # Grants
        # Prepare agency
        agency = Agency.objects.create(name="GA")
        # Prepare a grant with ids 1 and 2
        Grant.objects.create(start="2000", end="2001", agency=agency, number="1", author=P1,
                             title="Testing grant")
        Grant.objects.create(start="2001", end="2005", agency=agency, number="2", author=P2,
                             title="False grant")

    def test_detail(self):
        response = self.client.get('/Person_test/')
        self.assertContains(response, 'Test Person', count=1)
        self.assertContains(response, 'Ongoing PHD', count=1)
        self.assertContains(response, 'Finished MGR', count=1)
        self.assertQuerysetEqual(response.context['theses'], ['<Thesis: Finished MGR>', '<Thesis: Finished BC>'])
        self.assertQuerysetEqual(response.context['theses_ongoing'], ['<Thesis: Ongoing PHD>'])

    def test_articles(self):
        response = self.client.get('/Person_test/papers/')
        self.assertContains(response, 'First article', count=1)
        self.assertNotContains(response, 'False article')
        articles = ['<Article: First article>',
                    '<Article: It is hard to come up with some funny thing...>',
                    '<Article: Newest trends in writing django tests>']
        self.assertQuerysetEqual(response.context['publications'], articles)
        self.assertQuerysetEqual(response.context['publications_first'],
                                 ['<Article: First article>', '<Article: Newest trends in writing django tests>'])

    def test_students(self):
        response = self.client.get('/Person_test/students/')
        self.assertContains(response, 'Test Student', count=1)
        self.assertContains(response, 'Finished Student', count=1)
        self.assertNotContains(response, 'False Student')

    def test_courses(self):
        response = self.client.get('/Person_test/courses/')
        self.assertContains(response, 'Testing course', count=1)
        self.assertNotContains(response, 'False course')

    def test_courses_practical(self):
        # New testing person
        H3 = Human.objects.create(nickname='Person_practical')
        P3 = Person.objects.create(type='STAFF', first_name='Test', last_name='Practical', human=H3)
        # Prepare a course with P3 as practical
        Course.objects.get(pk=1).practical_lectors.add(P3)
        response = self.client.get('/Person_practical/courses/')
        self.assertContains(response, 'Testing course', count=1)

    def test_grants(self):
        response = self.client.get('/Person_test/grants/')
        self.assertContains(response, 'Testing grant', count=1)
        self.assertNotContains(response, 'False grant')

    def test_grants_coauthor(self):
        # New testing person
        H3 = Human.objects.create(nickname='Person3_test')
        P3 = Person.objects.create(type='STAFF', first_name='Test', last_name='Coauthor', human=H3)
        # Prepare a grant with P3 as coauthor
        Grant.objects.get(pk=1).co_authors.add(P3)
        response = self.client.get('/Person3_test/grants/')
        self.assertContains(response, 'Testing grant', count=1)


class TestEmptyDatabase(TestCase):
    def test_articles(self):
        # Should return 404
        response = self.client.get('/people/articles/')
        self.assertEqual(response.status_code, 404)

    def test_grants(self):
        # Should show empty page
        response = self.client.get('/people/grants/')
        self.assertContains(response, 'suggestion or more information', count=1)

    def test_people(self):
        # All of these should return empty page with the basic title
        response = self.client.get('/people/staff/')
        self.assertContains(response, '<h1>Academic staff</h1>', count=1, html=True)
        response = self.client.get('/people/phd/')
        self.assertContains(response, '<h1>PhD. students</h1>', count=1, html=True)
        response = self.client.get('/people/students/')
        self.assertContains(response, '<h1>Students</h1>', count=1, html=True)
        response = self.client.get('/people/other/')
        self.assertContains(response, '<h1>Other staff</h1>', count=1, html=True)
        response = self.client.get('/people/retired/')
        self.assertContains(response, '<h1>Former members</h1>', count=1, html=True)
        response = self.client.get('/people/graduates/')
        self.assertContains(response, '<h1>Graduate students</h1>', count=1, html=True)

    def test_theses(self):
        # Returns empty page
        response = self.client.get('/people/theses/')
        self.assertContains(response, 'suggestion or more information', count=1)

    def test_courses(self):
        # Returns empty page
        response = self.client.get('/people/courses/')
        self.assertContains(response, 'suggestion or more information', count=1)

    def test_downloads(self):
        # Returns empty page
        response = self.client.get('/people/downloads/')
        self.assertContains(response, 'suggestion or more information', count=1)
