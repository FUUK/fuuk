# -*- coding: utf-8 -*-
from distutils.core import setup


try:
    from subprocess import check_output
except ImportError:
    import subprocess
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


PACKAGES = ('fuuk', 'fuuk.people', 'fuuk.people.admin', 'fuuk.people.context_processors', 'fuuk.people.management',
            'fuuk.people.management.commands', 'fuuk.people.models', 'fuuk.people.templatetags')

PACKAGE_DATA = {'fuuk': ['locale/cs/LC_MESSAGES/*', 'people/fixtures/*.yaml' 'static/css/*', 'static/img/*',
                         'static/js/*', 'templates/*.html', 'templates/admin/*', 'templates/flatpages/*.html',
                         'templates/ofb/*.html', 'templates/oppo/*.html', 'templates/oppo/people/*.html',
                         'templates/oppo/people/person/*.html',
                         'templates/people/*.html', 'templates/people/person/*.html']}


def get_git_version():
    version = check_output(['git', 'describe', '--tags'])
    if version[-1] == '\n':
        version = version[:-1]
    return version


def main():
    version = get_git_version() or VERSION
    setup(name='Web OBF FUUK',
          version=version,
          author = 'Vlastimil Zíma',
          author_email = 'vlastimil.zima@gmail.com',
          description = 'Web for Division of Biomolecular Physics at Institute of Physics at Charles University',
          packages=PACKAGES,
          package_data=PACKAGE_DATA)


if __name__ == '__main__':
    main()
