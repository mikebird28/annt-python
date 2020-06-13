
test:
	python -m unittest discover test

build:
	python setup.py sdist

clean:
	-rm -rf annt.egg-info
	-rm -rf dist
	-rm MANIFEST

.PHONY: test build clean