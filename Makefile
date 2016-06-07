.DEFAULT_GOAL := test

init:
	pip install -r requirements.txt

test:
	py.test tests
