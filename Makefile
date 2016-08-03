.DEFAULT_GOAL := test

init:
	pip install -r requirements.txt

integration:
	py.test -s \
		tests/integration/test_domains.py \
		tests/integration/test_records.py \
		tests/integration/test_contacts.py \
		tests/integration/test_registrations.py

test:
	py.test tests/unit

all: test integration

.PHONY: init integration test all
