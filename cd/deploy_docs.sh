#!/usr/bin/env sh
mkdir /tmp/gh-pages
cp -r docs/build/html /tmp/gh_pages
git checkout gh-pages
rm -rf * && cp -r /tmp/gh-pages/* ./ && rm -rf /tmp/gh-pages && git add . && git commit -m "Updated gh-pages" && git push && git checkout -
