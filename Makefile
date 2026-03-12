PYTHON ?= python3

.PHONY: run test
run:
	$(PYTHON) 04-functions/stmt3.py < 04-functions/fac.st3

test:
	./test.sh
