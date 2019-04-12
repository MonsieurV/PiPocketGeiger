install-dev:
	pipenv install

lint:
	pipenv run flake8 PiPocketGeiger examples
	pipenv run pylint PiPocketGeiger

format:
	pipenv run black PiPocketGeiger examples

release:
	pipenv run python setup.py sdist
	pipenv run python setup.py bdist_wheel --universal
	pipenv run twine upload dist/*
