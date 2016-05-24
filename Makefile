# All targets are phony
.PHONY: test pylint pepify isort i18n check-isort check-flake8 check-test check-migrations

# Tests for development
test:
	PYTHONPATH="settings::${PYTHONPATH}" DJANGO_SETTINGS_MODULE='test_settings' python -W all fuuk/manage.py test fuuk

pylint:
	-pylint fuuk --reports=no

pepify: pylint check-flake8

isort:
	isort --recursive fuuk

i18n:
	cd fuuk && ${DJANGO_ADMIN} makemessages -l cs
	msgattrib --no-obsolete --no-location --sort-output -o fuuk/locale/cs/LC_MESSAGES/django.po fuuk/locale/cs/LC_MESSAGES/django.po

check-isort:
	isort --check-only --diff --recursive fuuk

check-flake8:
	flake8 --format=pylint fuuk

# Tests in travis - only adds 'settings' to PYTHONPATH and runs tests on installed `fuuk`
check-test:
	PYTHONPATH="settings" DJANGO_SETTINGS_MODULE='test_settings' python -W all fuuk/manage.py test fuuk

check-migrations:
	test "$$(PYTHONPATH='settings::${PYTHONPATH}' DJANGO_SETTINGS_MODULE='test_settings' python fuuk/manage.py makemigrations --noinput --dry-run 2> /dev/null)" = "No changes detected"
