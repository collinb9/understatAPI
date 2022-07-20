#!/usr/bin/env sh
mkdir temp/gh-pages
cp -r docs/build/html temp/gh_pages
git checkout gh-pages
cd .. && rm -rf * && cp -r /tmp/gh-pages/* ./ && rm -rf /tmp/gh-pages && git add . && git commit -m "Updated gh-pages" && git push && git checkout master

