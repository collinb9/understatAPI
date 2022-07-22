#!/usr/bin/env sh

set -e
set -x

mkdir -p /tmp/gh-pages
cp -r docs/build/html /tmp/gh-pages
git checkout gh-pages
git pull
rm -rf * && \
    cp -r /tmp/gh-pages/html/* ./ && \
    rm -rf /tmp/gh-pages && git add . && \
    git commit -m "Updated gh-pages" && \
    git push && \
    git checkout -

