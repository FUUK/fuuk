# -*- coding: utf-8 -*-
from distutils.core import setup

from fuuk import __version__


PACKAGES = ('fuuk', 'fuuk.people', 'fuuk.people.admin', 'fuuk.people.context_processors', 'fuuk.people.management',
            'fuuk.people.management.commands', 'fuuk.people.models', 'fuuk.people.templatetags')

PACKAGE_DATA = {'fuuk': ['locale/cs/LC_MESSAGES/*', 'templates/*.html', 'templates/admin/*',
                         'templates/flatpages/*.html', 'templates/magnet/*.html',
                         'templates/ofb/*.html', 'templates/oppo/*.html', 'templates/oppo/people/*.html',
                         'templates/oppo/people/person/*.html',
                         'templates/people/*.html', 'templates/people/person/*.html', 'templates/theory/*.html'],
                'fuuk.people': ['fixtures/*.yaml', 'static/css/*', 'static/img/*', 'static/js/*']}


def main():
    setup(name='Web FUUK',
          version=__version__,
          author='Vlastimil Zíma',
          author_email='vlastimil.zima@gmail.com',
          description='Web of Institute of Physics at Charles University',
          packages=PACKAGES,
          package_data=PACKAGE_DATA)


if __name__ == '__main__':
    main()
