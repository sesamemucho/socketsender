.PHONY: help clean clean-pyc clean-build list isort test test-all black docs release sdist wheel

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "format - format code using black"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 src test

test:
	pytest --color=no --cov-report term-missing --cov=src --cov=tests tests

isort:
	isort --check-only --diff --recursive --skip .tox --skip .venv --skip build -m 3 -tc

test-all:
	tox

format:
	black tests src

docs:
	rm -f docs/socketsender.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ src/socketsender
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
#	open docs/_build/html/index.html

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

sdist: clean
	python setup.py sdist
	python setup.py bdist_wheel upload
	ls -l dist

wheel: clean
	python setup.py bdist_wheel
