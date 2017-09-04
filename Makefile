venv/dev: venv/dev/bin/activate

venv/dev/bin/activate: setup.py
	test -d venv || virtualenv venv
	venv/bin/pip install -e .[dev]
	touch venv/bin/activate

install-dev: venv/dev

lint:
	venv/bin/flake8 PiPocketGeiger examples
	venv/bin/pylint PiPocketGeiger examples/*.py
