test:
	@py.test

vtest:
	@py.test -v

ptest:
	@py.test -s

script:
	@cat msc.log | healthcheck/check.py

.PHONY: test vtest ptest script
