#!/usr/bin/env sh

set -e

python -m pip install build twine
python -m build
twine upload -r dist/* --repository pypi
