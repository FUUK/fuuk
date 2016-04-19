DJANGO_ADMIN = django-admin


# Tests for development
test:
	PYTHONPATH="settings::${PYTHONPATH}" DJANGO_SETTINGS_MODULE='test_settings' python -W all fuuk/manage.py test fuuk

pylint:
	-pylint fuuk --reports=no

flake8:
	-flake8 fuuk

pepify: pylint flake8

isort:
	isort --recursive fuuk

i18n:
	cd fuuk && ${DJANGO_ADMIN} makemessages -l cs
	msgattrib --no-obsolete --no-location --sort-output -o fuuk/locale/cs/LC_MESSAGES/django.po fuuk/locale/cs/LC_MESSAGES/django.po

check-isort:
	isort --check-only --diff --recursive fuuk

# Tests in travis - only adds 'settings' to PYTHONPATH and runs tests on installed `fuuk`
check-test:
	PYTHONPATH="settings" DJANGO_SETTINGS_MODULE='test_settings' python -W all fuuk/manage.py test fuuk
