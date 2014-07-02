# -*- coding: utf-8 -*-
import subprocess
import sys

from distutils import log
from distutils.command.build_py import build_py
from distutils.core import setup
from distutils.dep_util import newer

from fuuk import __version__


PACKAGES = ('fuuk', 'fuuk.common', 'fuuk.common.templatetags', 'fuuk.people', 'fuuk.people.admin',
            'fuuk.people.context_processors', 'fuuk.people.management', 'fuuk.people.management.commands',
            'fuuk.people.models', 'fuuk.people.templatetags')

PACKAGE_DATA = {'fuuk': ['locale/cs/LC_MESSAGES/*', 'templates/*.html', 'templates/admin/*',
                         'templates/flatpages/*.html', 'templates/magnet/*.html',
                         'templates/ofb/*.html', 'templates/oppo/*.html', 'templates/oppo/people/*.html',
                         'templates/oppo/people/person/*.html',
                         'templates/people/*.html', 'templates/people/person/*.html', 'templates/theory/*.html'],
                'fuuk.people': ['fixtures/*.yaml', 'static/css/*', 'static/img/*', 'static/js/*']}


class i18n_build_py(build_py):
    """
    Distuutils `build_py` command which compiles also gettext files.
    """
    def byte_compile(self, files):
        build_py.byte_compile(self, files)

        # Skip compiling
        if sys.dont_write_bytecode:
            return

        for pofile in files:
            if pofile[-3:] != ".po":
                # Don't compile anything else
                continue
            mofile = pofile[:-3] + '.mo'
            if self.force or newer(pofile, mofile):
                log.info("byte-compiling %s to %s", pofile, mofile)
                if not self.dry_run:
                    subprocess.check_call(['msgfmt', '-o', mofile, pofile])
            else:
                log.debug("skipping byte-compilation of %s to %s",
                          pofile, mofile)


def main():
    setup(name='Web FUUK',
          version=__version__,
          author='Vlastimil Zíma',
          author_email='vlastimil.zima@gmail.com',
          description='Web of Institute of Physics at Charles University',
          packages=PACKAGES,
          package_data=PACKAGE_DATA,
          cmdclass={'build_py': i18n_build_py})


if __name__ == '__main__':
    main()
