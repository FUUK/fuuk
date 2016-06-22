# -*- coding: utf-8 -*-
from datetime import date

from django.db.models import Count
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from fuuk.people.models import Article, Course, Grant, Human, Person, Thesis


class ArticleList(ListView):

    paginate_by = 50
    allow_empty = False

    def get_queryset(self):
        queryset = Article.objects.filter(type__in=('ARTICLE', 'BOOK'))
        self.years = queryset.values_list('year', flat=True).annotate(Count('year')).order_by('-year')
        try:
            self.year = int(self.kwargs['year'])
        except (ValueError, KeyError):
            if self.years.exists():
                self.year = self.years[0]
            else:
                raise Http404
        return queryset.filter(year=self.year).order_by('-year', 'title')

    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        context['year'] = self.year
        context['years'] = self.years
        return context


class GrantList(ListView):

    def get_queryset(self):
        return Grant.objects.filter(end__gte=date.today().year).order_by('-end', '-pk')

    def get_context_data(self, **kwargs):
        context = super(GrantList, self).get_context_data(**kwargs)
        context['grants_finished'] = Grant.objects.filter(end__gte=(date.today().year - 2),
                                                          end__lt=date.today().year).order_by('-end', '-pk')
        return context


class ThesisList(ListView):

    def get_queryset(self):
        self.year = self.request.GET.get('year', None)
        self.type = self.request.GET.get('type', None)

        queryset = Thesis.objects.filter(defended=True)

        if self.year:
            queryset = queryset.filter(year=int(self.year)).order_by('-type')
        if self.type:
            queryset = queryset.filter(type=self.type.upper()).order_by('-year')

        # annotate on values_list with flat=True does not work properly in Django 1.8 due to a bug in modeltransaltion
        # self.types = Thesis.objects.filter(defended=True).values_list('type', flat=True).annotate(Count('type'))
        #                    .order_by('-type')
        # self.years = Thesis.objects.filter(defended=True).values_list('year', flat=True).annotate(Count('year'))
        #                    .order_by('-year')
        self.types = [i[0] for i in Thesis.objects.filter(defended=True).values_list('type').annotate(Count('type'))
                                          .order_by('-type')]
        self.years = [i[0] for i in Thesis.objects.filter(defended=True).values_list('year').annotate(Count('year'))
                                          .order_by('-year')]

        # we got filter but no results
        if self.year or self.type:
            if not queryset:
                raise Http404
        else:
            queryset = queryset.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ThesisList, self).get_context_data(**kwargs)
        context['types'] = [(type, Thesis(type=type).get_type_display()) for type in self.types]
        context['years'] = self.years
        context['year'] = self.year
        context['type'] = self.type
        return context


class PeopleList(ListView):

    people_type = None
    title = None

    def get_context_data(self, **kwargs):
        context = super(PeopleList, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def get_queryset(self):
        return Person.objects.filter(type=self.people_type, is_active=True).order_by('last_name')


class StudentList(ListView):

    template_name = 'people/students.html'
    queryset = Person.objects.filter(type='MGR', is_active=True).order_by('last_name')

    def get_context_data(self, **kwargs):
        context = super(StudentList, self).get_context_data(**kwargs)
        context['bachelors'] = Person.objects.filter(type='BC', is_active=True).order_by('last_name')
        context['students'] = Person.objects.filter(type='STUDENT', is_active=True).order_by('last_name')
        return context


class RetiredList(ListView):

    queryset = Person.objects.filter(type__in=('STAFF', 'OTHER'), is_active=False).order_by('last_name')

    def get_context_data(self, **kwargs):
        context = super(RetiredList, self).get_context_data(**kwargs)
        context['title'] = _('Former members')
        return context


###############################################################################
# Person pages
class PersonMixin(object):
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super(PersonMixin, self).get_context_data(**kwargs)
        human_qs = Human.objects.filter(nickname=self.kwargs['slug'])
        if not human_qs.exists():
            raise Http404
        else:
            human = human_qs[0]

        publications_first = Article.objects.filter(author__order=1, author__person__human=human).order_by('-year')
        grants_author = Grant.objects.filter(author__human=human, end__gte=date.today().year) \
            .values_list('pk', flat=True)
        grants_co_author = Grant.objects.filter(co_authors__human=human, end__gte=date.today().year) \
            .values_list('pk', flat=True)
        grants_finished_author = Grant.objects.filter(author__human=human, end__lt=date.today().year) \
            .values_list('pk', flat=True)
        grants_finished_co_author = Grant.objects.filter(co_authors__human=human, end__lt=date.today().year) \
            .values_list('pk', flat=True)
        grants_finished = Grant.objects.filter(pk__in=grants_finished_author | grants_finished_co_author) \
            .order_by('-end', '-pk')
        students_finished = Person.objects.filter(advisor__human=human, is_active=False) \
            .order_by('last_name', 'first_name')
        context.update({
            'human': human,
            'person': human.person_set.order_by('-is_active')[0],
            'publications': Article.objects.filter(author__person__human=human).order_by('-year', 'title'),
            'publications_first': publications_first,
            'courses': Course.objects.filter(lectors__human=human).order_by('pk'),
            'courses_practical': Course.objects.filter(practical_lectors__human=human).order_by('pk'),
            'students': Person.objects.filter(advisor__human=human, is_active=True).order_by('last_name', 'first_name'),
            'students_finished': students_finished,
            'grants': Grant.objects.filter(pk__in=grants_author | grants_co_author).order_by('-end', '-pk'),
            'grants_finished': grants_finished,
        })
        return context


class PersonListView(ListView):
    slug_field = None

    def get_queryset(self):
        query = {self.slug_field: self.kwargs['slug']}
        queryset = super(PersonListView, self).get_queryset().filter(**query)
        if self.get_allow_empty() and not queryset.exists():
            raise Http404
        return queryset


class PersonDetail(PersonMixin, DetailView):

    template_name = 'people/person/detail.html'
    queryset = Person.objects.filter(is_active=True)
    slug_field = 'human__nickname'

    def get_context_data(self, **kwargs):
        context = super(PersonDetail, self).get_context_data(**kwargs)
        context['theses'] = Thesis.objects.filter(author__human=self.object.human, defended=True).order_by('-year')
        context['theses_ongoing'] = Thesis.objects.filter(author__human=self.object.human, defended=False) \
            .order_by('-year')
        return context


class PersonArticles(PersonMixin, ListView):
    '''
    Get people articles

    @ivar first: If only papers with Person as a first author shoudl be displayed
    '''
    template_name = 'people/person/articles.html'
    model = Article
    first = False

    def get_context_data(self, **kwargs):
        context = super(PersonArticles, self).get_context_data(**kwargs)
        if context['human'].display_posters:
            presentation_types = ['POSTER', 'TALK', 'INVITED']
        else:
            presentation_types = ['TALK', 'INVITED']
        if self.first:
            context['articles'] = context['publications_first'].filter(type='ARTICLE')
        else:
            context['articles'] = context['publications'].filter(type='ARTICLE')
        if context['human'].display_talks:
            context['presentations'] = context['publications'].filter(type__in=presentation_types)
        else:
            context['presentations'] = context['publications'].filter(type__in=presentation_types) \
                .filter(presenter__human=context['person'].human)
        context['books'] = context['publications'].filter(type='BOOK')
        return context


class PersonCourses(PersonMixin, PersonListView):

    template_name = 'people/person/courses.html'
    model = Course

    def get_queryset(self):
        nick = self.kwargs['slug']
        courses_lector = Course.objects.filter(lectors__human__nickname=nick).values_list('pk', flat=True)
        courses_practical = Course.objects.filter(practical_lectors__human__nickname=nick).values_list('pk', flat=True)
        return self.model.objects.filter(pk__in=courses_lector | courses_practical)


class PersonStudents(PersonMixin, PersonListView):

    template_name = 'people/person/students.html'
    model = Person
    slug_field = 'advisor__human__nickname'


class PersonGrants(PersonMixin, PersonListView):

    template_name = 'people/person/grants.html'
    model = Grant

    def get_queryset(self):
        '''
        Lookup grants by author or coauthor.
        '''
        nick = self.kwargs['slug']
        grants_author = Grant.objects.filter(author__human__nickname=nick).values_list('pk', flat=True)
        grants_co_author = Grant.objects.filter(co_authors__human__nickname=nick).values_list('pk', flat=True)
        return self.model.objects.filter(pk__in=grants_author | grants_co_author)


class Papers(PersonMixin, ListView):

    template_name = 'people/papers.html'
    queryset = Article.objects.filter(type__in=('ARTICLE', 'BOOK')).order_by('-year')
