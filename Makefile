.DEFAULT_GOAL := test

env: env/bin/activate

env/bin/activate: requirements.txt
	test -d env || virtualenv env;	\
  ./env/bin/pip install -r requirements.txt --upgrade;	\

dnsimple.egg-info/SOURCES.txt: env
	./env/bin/python setup.py develop

dev: dnsimple.egg-info/SOURCES.txt

integration: dev
	./env/bin/py.test -s tests/integration/test_{domains,records}.py

test: dev
	./env/bin/py.test tests/unit

all: test integration

.PHONY: dev integration test all
