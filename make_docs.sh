pip install -r docs/requirements.txt
sphinx-apidoc --separate -f -o docs/source . ./setup.py ./test
make -C docs/ html
