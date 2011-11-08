# -*- coding: utf-8 -*-
import os

from distutils.core import setup
from subprocess import check_output


VERSION = '1.0.0'


def get_git_version():
    version = check_output(['git', 'describe', '--tags'])
    if version[-1] == '\n':
        version = version[:-1]
    return version


def get_data_files(directories):
    walks = []
    for directory in directories:
        walks.extend(os.walk(directory))

    return [
        (path, map(lambda x: os.path.join(path, x), files)) 
        for path, dir, files in walks
    ]


def main():
    version = get_git_version() or VERSION
    setup(
        name = 'Web OBF FUUK',
        version=version,
        author = 'Vlastimil Zíma',
        author_email = 'vlastimil.zima@gmail.com',
        description = 'Web for Division of Biomolecular Physics at Institute of Physics at Charles University',
        packages = [
            '',
            'people', 'people.admin', 'people.models', 'people.templatetags','people.context_processors',
        ],
        data_files = get_data_files(('locale', 'media', 'people/fixtures', 'templates', 'sql_update')),
    )


if __name__ == '__main__':
    main()
