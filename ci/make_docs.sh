#!/usr/bin/env sh

if [ -d "docs/build" ]; then
    rm -rf docs/build
fi
sphinx-apidoc --separate -f -o docs/source . ./setup.py ./test
make -C docs/ html
