.DEFAULT_GOAL := test

init:
	pip install -r requirements.txt

integration:
	py.test -s tests/integration/test_domains.py tests/integration/test_records.py

test:
	py.test tests/unit
