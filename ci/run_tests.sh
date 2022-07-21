#!/usr/bin/env sh

set -e
CHANGED_FILES=`git diff --name-only --diff-filter=d origin/master | grep -E '\.py$' | tr '\n' ' '`
echo $CHANGED_FILES
if [ -z "$CHANGED_FILES" ]
then
		export CHANGED_FILES="understatapi/api.py"
fi
black --check --line-length=79 ${CHANGED_FILES}
pylint ${CHANGED_FILES}
mypy -p understatapi
coverage run -m unittest discover
coverage report --fail-under=100
make -C docs/ doctest
