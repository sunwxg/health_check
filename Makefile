test:
	@py.test

vtest:
	@py.test -v

ptest:
	@py.test -s

script:
	@cat msc.log | ./py.hc
	@cat mgw.log | ./py.hc mgw

install:
	@python setup.py install --record 1.log

uninstall:
	@cat 1.log |xargs -I {} rm -rf {}
	@rm -rf 1.log

.PHONY: test vtest ptest script install uninstall
