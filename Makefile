# All targets are phony
.PHONY: test pylint pepify isort i18n check-isort check-flake8 check-test check-migrations check-i18n

PO_FILE = fuuk/locale/cs/LC_MESSAGES/django.po
FUFLATPAGES_PO_FILE = fuuk/fuflatpages/locale/cs/LC_MESSAGES/django.po

# Tests for development
test:
	PYTHONPATH="settings::${PYTHONPATH}" DJANGO_SETTINGS_MODULE='test_settings' python -W all fuuk/manage.py test fuuk

pylint:
	-pylint fuuk --reports=no

pepify: pylint check-flake8

isort:
	isort --recursive fuuk

i18n:
	cd fuuk && django-admin makemessages -l cs --no-obsolete --no-location
	msgattrib --sort-output -o ${FUFLATPAGES_PO_FILE} ${FUFLATPAGES_PO_FILE}
	msgattrib --sort-output -o ${PO_FILE} ${PO_FILE}

check-isort:
	isort --check-only --diff --recursive fuuk

check-flake8:
	flake8 --format=pylint fuuk

# Tests in travis - only adds 'settings' to PYTHONPATH and runs tests on installed `fuuk`
check-test:
	PYTHONPATH="settings" DJANGO_SETTINGS_MODULE='test_settings' python -W all fuuk/manage.py test fuuk

check-migrations:
	! PYTHONPATH='settings::${PYTHONPATH}' DJANGO_SETTINGS_MODULE='test_settings' python fuuk/manage.py makemigrations --noinput --dry-run --exit

check-i18n:
	# Make sure there are no obsolete entries
	python -c "import polib; po = polib.pofile('${PO_FILE}'); exit(int(bool(po.obsolete_entries())))"
	python -c "import polib; po = polib.pofile('${FUFLATPAGES_PO_FILE}'); exit(int(bool(po.obsolete_entries())))"
	# Make sure there are no fuzzy entries
	python -c "import polib; po = polib.pofile('${PO_FILE}'); exit(int(bool(po.fuzzy_entries())))"
	python -c "import polib; po = polib.pofile('${FUFLATPAGES_PO_FILE}'); exit(int(bool(po.fuzzy_entries())))"
	# Make sure there are no untranslated entries
	python -c "import polib; po = polib.pofile('${PO_FILE}'); exit(int(bool(po.untranslated_entries())))"
	python -c "import polib; po = polib.pofile('${FUFLATPAGES_PO_FILE}'); exit(int(bool(po.untranslated_entries())))"
	# Make sure there are no locations
	python -c "import polib; po = polib.pofile('${PO_FILE}'); exit(int(bool([e for e in po if e.occurrences])))"
	python -c "import polib; po = polib.pofile('${FUFLATPAGES_PO_FILE}'); exit(int(bool([e for e in po if e.occurrences])))"
	# Make sure translations are ordered
	python -c "import polib; po = polib.pofile('${PO_FILE}'); exit(int(bool([e.msgid for e in po] != sorted([e.msgid for e in po]))))"
	python -c "import polib; po = polib.pofile('${FUFLATPAGES_PO_FILE}'); exit(int(bool([e.msgid for e in po] != sorted([e.msgid for e in po]))))"
	# Make sure catalog is complete - make C locales to generate POT files and compare it using the msgcmp
	cd fuuk && django-admin makemessages -l C --no-obsolete --no-location --keep-pot
	msgcmp ${PO_FILE} fuuk/locale/django.pot
	msgcmp ${FUFLATPAGES_PO_FILE} fuuk/fuflatpages/locale/django.pot
	-rm -r fuuk/locale/django.pot fuuk/locale/C fuuk/fuflatpages/locale/django.pot fuuk/fuflatpages/locale/C
