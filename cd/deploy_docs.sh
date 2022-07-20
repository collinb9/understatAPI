#!/usr/bin/env sh
mkdir -p /tmp/gh-pages
cp -r docs/build/html /tmp/gh-pages
git checkout gh-pages
git rm -rf * && cp -r /tmp/gh-pages/html/* ./ && rm -rf /tmp/gh-pages && git add . && git commit -m "Updated gh-pages" && git push && git checkout -

