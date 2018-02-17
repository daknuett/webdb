
all: test

.PHONY: test
test: install
	pytest -vv test/

.PHONY: install
install:
	python3 setup.py install

print-contributors:
	python3 tools/contributors.py print contributors.yml 

