test:
	@py.test

vtest:
	@py.test -v

script:
	@cat msc.log | healthcheck/check.py

.PHONY: test vtest script
