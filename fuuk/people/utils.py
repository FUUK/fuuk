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
