# NOTE:  This file MUST use tabs for indentation rather than spaces
#        If you get an error "*** missing separator. Stop" then you
#        probably have spaces for indentation.
#
# In PyCharm, you can install a plugin for Makefile support that
# will use tabs
export PATH:=${PWD}/.venv/bin:${PATH};

all: test static

test:
	pytest;

static:
	flake8 src tests;
	pycodestyle src tests;
	pylint src tests;

clean:
	rm -rf htmlcov
	rm -f unit-python.xml
	rm -f .coverage
	# find and remove all __pycache__ folders and all .pyc files (compiled python)
	find . | grep -E "(__pycache__|\.pyc)" | xargs rm -rf
	rm -rf .pytest_cache
