DJANGO_ADMIN = django-admin


i18n:
	cd fuuk && ${DJANGO_ADMIN} makemessages -l cs
	msgattrib --no-obsolete --no-location --sort-output -o fuuk/locale/cs/LC_MESSAGES/django.po fuuk/locale/cs/LC_MESSAGES/django.po
