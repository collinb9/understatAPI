#!/usr/bin/env sh

set -e
set -x

mkdir -p /tmp/gh-pages
cp -r docs/build/html /tmp/gh-pages
git checkout -b gh-pages
rm -rf * && \
    cp -r /tmp/gh-pages/html/* ./ && \
    rm -rf /tmp/gh-pages && git add . && \
    git commit -m "Updated gh-pages" && \
    git push --set-upstream origin gh-pages && \
    git checkout -

