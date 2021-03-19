sphinx-apidoc --separate -f -o docs/source . ./setup.py ./test
make -C docs/ html
