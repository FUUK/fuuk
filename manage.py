#!/usr/bin/env python

import sys
from optparse import OptionParser, make_option
settings_module = OptionParser(option_list=[make_option('--settings')]).parse_args(sys.argv[:])[0].settings

from django.core.management import execute_manager

if not settings_module: 
    try:
        import settings # Assumed to be in the same directory.
    except ImportError:
        import sys
        sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
        sys.exit(1)
else:
    settings = __import__(settings_module)

if __name__ == "__main__":
    execute_manager(settings)
