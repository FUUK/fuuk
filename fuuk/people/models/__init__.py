"""Modules related to people"""
from fuuk.people.models.place import Department, Place
from fuuk.people.models.person import Human, Person
from fuuk.people.models.course import Course, Attachment
from fuuk.people.models.grant import Grant, Agency
from fuuk.people.models.article import ARTICLE_TYPES, Article, Author, ArticleBook, ArticleArticle, ArticleConference
from fuuk.people.models.thesis import Thesis
from fuuk.people.models.news import News

__all__ = ['ARTICLE_TYPES', 'Agency', 'Article', 'ArticleArticle', 'ArticleBook', 'ArticleConference', 'Attachment',
           'Author', 'Course', 'Department', 'Grant', 'Human', 'News', 'Person', 'Place', 'Thesis']
