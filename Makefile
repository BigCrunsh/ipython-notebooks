.PHONY: all
all: build lint test

# http://pylint-messages.wikidot.com/all-messages
pylinter = pylint \
	--reports n \
	--disable=E0611 \
	--disable=E1101 \
	--disable=E1103 \
	--disable=W0511 \
	--min-public-methods=0 \
	$(1)

.PHONY: test
test: build
	nosetests --where tests

.PHONY: lint
lint: build
	$(call pylinter,projects)
	$(call pylinter,tests)

.PHONY: build
build:
	python setup.py install

.PHONY: clean
clean:
	rm -rf analysis.egg-info/
	rm -rf build/
	rm -rf dist/
	find . -name '*.pyc' -delete
