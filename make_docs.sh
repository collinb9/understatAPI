sphinx-apidoc --separate -f -o docs/source . ./setup.py ./test
make -C docs/ html
touch docs/build/html/.nojekyll
