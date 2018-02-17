
all: test doc

.PHONY: test
test: install
	pytest -vv test/

.PHONY: install
install:
	python3 setup.py install

print-contributors:
	python3 tools/contributors.py print contributors.yml 

create-contributors:
	python3 tools/contributors.py create contributors.yml doc/source/contributors.rst

doc: install create-contributors
	cd doc && make html
