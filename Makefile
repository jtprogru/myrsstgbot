install-dev-deps: dev-deps
	pip-sync requirements/base.txt requirements/dev.txt

install-deps: deps
	pip-sync requirements/base.txt

deps:
	pip install --upgrade pip pip-tools
	pip-compile requirements/base.in

dev-deps: deps
	pip-compile requirements/dev.in

fetchdb:
	scp borshev.com:/srv/pmdaily/storage/pmdaily.sqlite storage/
	cd src && ./manage.py anonymize_db

server:
	cd src && ./manage.py migrate && ./manage.py runserver

worker:
	cd src && celery -A app worker -E --purge

lint:
	flake8 src

test:
	cd src && pytest -n 4 --ff -x && pytest --dead-fixtures

coverage:
	cd src && pytest --dead-fixtures && pytest --cov-report=xml --cov=. -n4 -x

checkmigrations:
	cd src && ./manage.py makemigrations --check --no-input --dry-run
