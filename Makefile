install-dev:
	pipenv install --dev

lint:
	pipenv run flake8 PiPocketGeiger examples
	pipenv run pylint PiPocketGeiger

format:
	pipenv run black PiPocketGeiger examples setup.py

release:
	pipenv run python setup.py sdist
	pipenv run python setup.py bdist_wheel --universal
	pipenv run twine check dist/*
	pipenv run twine upload dist/*
