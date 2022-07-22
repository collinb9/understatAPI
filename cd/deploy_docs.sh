#!/usr/bin/env sh

set -e

generate_circleci_config()
{
  cat <<EOF
workflows:
  build-workflow:
    jobs:
      - build:
          filters:
            branches:
              ignore: /.*/
EOF
}

mkdir -p /tmp/gh-pages
cp -r docs/build/html /tmp/gh-pages
git checkout gh-pages
git pull
rm -rf * && \
    cp -r /tmp/gh-pages/html/* ./ && \
    mkdir -p .circleci \\
    generate_circleci_config > .circleci/config.yml \\
    rm -rf /tmp/gh-pages && git add . && \
    git commit -m "Updated gh-pages" && \
    git push && \
    git checkout -

