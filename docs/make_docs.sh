sphinx-apidoc --separate -f -o docs/source . ./setup.py ./test
cd docs && make html 