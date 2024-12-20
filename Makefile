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

docker-build:
	docker build -t leaderboards_scraper .

docker-run:
	docker run -v $(PWD)/data:/usr/src/app/data --rm leaderboards_scraper

test:
	pytest --flake8 --black --cov=leaderboards_scraper --cov-report term-missing tests/

run:
	python -m leaderboards_scraper.main

release-test: clean
	python setup.py sdist bdist_wheel
	twine upload --repository pypitest dist/*

release-prod: clean
	python setup.py sdist bdist_wheel
	twine upload --repository pypi dist/*

t: test
r: run
