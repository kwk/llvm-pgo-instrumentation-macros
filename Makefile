# Prepare variables
TMP = $(CURDIR)/tmp
NAME=$(shell basename $(CURDIR))
VERSION = $(shell grep ^Version $(NAME).spec | sed 's/.* //')
PACKAGE = $(NAME)-$(VERSION)

.PHONY: rpm, srpm, clean

rpm:
	fedpkg --release f37 --name $(NAME) local -- --noclean
srpm:
	fedpkg --release f37 --name $(NAME) srpm
clean:
	rm -rf $(PACKAGE)* noarch tmp
