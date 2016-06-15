"""
Modified version of `django.contrib.flatpages`.

Since the flatpages can't be used as a library, code is copied from Django directly.

Differences from Django flatpages:
 * Translations
 * Neither middleware nor template tag are available.
"""
default_app_config = 'fuuk.fuflatpages.apps.FlatPagesConfig'
