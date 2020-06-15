
test:
	python -m unittest discover test

build:
	python setup.py sdist
	python setup.py bdist_wheel

deploy-test:
	@echo "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	python3 -m twine upload --repository testpypi dist/*

deploy-release:
	@echo "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	python3 -m twine upload --repository pypi dist/*

clean:
	-rm -rf annt.egg-info
	-rm -rf dist
	-rm MANIFEST

.PHONY: test build clean