"""Modules related to people"""
from .place import Department, Place, Institution
from .person import Human, Person
from .course import Course, Attachment
from .grant import Grant, Agency, GrantCollaborator
from .article import ARTICLE_TYPES, Article, Author, ArticleBook, ArticleArticle, ArticleConference
from .thesis import Thesis
from .news import News

__all__ = ['ARTICLE_TYPES', 'Agency', 'Article', 'ArticleArticle', 'ArticleBook', 'ArticleConference', 'Attachment',
           'Author', 'Course', 'Department', 'Grant', 'GrantCollaborator', 'Human', 'Institution', 'News', 'Person',
           'Place', 'Thesis']
