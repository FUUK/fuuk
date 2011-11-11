# -*- coding: utf-8 -*-
import os

from distutils.core import setup

try:
    from subprocess import check_output
except ImportError:
    def check_output(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd, output=output)
        return output

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
