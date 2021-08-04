default: test

clean: clean-build clean-pyc

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

init:
	pipenv install

init-dev:
	pipenv install -d

run-test:
	pipenv run pytest --flake8 --black --cov=smb3_leaderboards --cov-report term-missing tests/

release-test: clean
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload --repository pypitest dist/*

release-prod: clean
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload --repository pypi dist/*

t: run-test
test: init-dev t
