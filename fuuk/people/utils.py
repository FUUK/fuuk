'''
Common utils for people.
'''
import os

from django.utils.encoding import force_text
from django.utils.text import slugify


def sanitize_filename(filename, path=''):
    '''
    Sanitize filename and create correct path.
    '''
    base, ext = os.path.splitext(force_text(filename))
    basename = slugify(base)
    if ext:
        basename += os.extsep + slugify(ext)
    return os.path.join(path, basename)


def full_name(prefix, first_name, last_name, suffix):
    '''Returns concatenated name, prefix and suffix can be None.'''
    return u"%s%s %s%s" % (
        prefix and u"%s " % prefix or u"",
        first_name, last_name,
        suffix and u", %s" % suffix or u"",
    )
