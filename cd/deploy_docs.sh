#!/usr/bin/env sh

set -e

mkdir -p /tmp/gh-pages
cp -r docs/build/html /tmp/gh-pages
git checkout gh-pages
rm -rf * && \
    cp -r /tmp/gh-pages/html/* ./ && \
    rm -rf /tmp/gh-pages && git add . && \
    git commit -m "Updated gh-pages" && \
    git push -q https://${GITHUB__TOKEN}@github.com/collinb9/understatapi.git gh-pages && \
    git checkout -

