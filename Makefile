# convenience makefile to boostrap & run buildout
# use `make options=-v` to run buildout with extra options

python = python2.7
options =

all: docs tests

coverage: htmlcov/index.html

htmlcov/index.html: README.rst src/dgr/buildout/*.py bin/coverage
	@bin/coverage run --source=./src/dgr/buildout/ --branch bin/test
	@bin/coverage html -i
	@touch $@
	@echo "Coverage report was generated at '$@'."

docs: docs/html/index.html

docs/html/index.html: docs/*.rst src/dgr/buildout/*.py src/dgr/buildout/browser/*.py src/dgr/buildout/tests/*.py bin/sphinx-build
	bin/sphinx-build -W docs docs/html
	@touch $@
	@echo "Documentation was generated at '$@'."

bin/sphinx-build: .installed.cfg
	@touch $@

.installed.cfg: bin/buildout buildout.cfg buildout.d/*.cfg setup.py
	bin/buildout $(options)

bin/buildout: bin/python buildout.cfg bootstrap.py
	bin/python bootstrap.py
	@touch $@

bin/python:
	virtualenv -p $(python) --no-site-packages .
	@touch $@

tests: .installed.cfg
	@bin/test
	@bin/flake8 setup.py
	@bin/flake8 src/dgr/buildout
	@for pt in `find src/dgr/buildout -name "*.pt"` ; do bin/zptlint $$pt; done
	@for xml in `find src/dgr/buildout -name "*.xml"` ; do bin/zptlint $$xml; done
	@for zcml in `find src/dgr/buildout -name "*.zcml"` ; do bin/zptlint $$zcml; done

clean:
	@rm -rf .coverage .installed.cfg .mr.developer.cfg bin docs/html htmlcov parts develop-eggs \
		src/dgr.buildout.egg-info lib include .Python

.PHONY: all docs tests clean
