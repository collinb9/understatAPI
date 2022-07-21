#!/usr/bin/env sh

set -e

version=$1
branch=master
repo=understatapi
owner=collinb9
token=$GITHUB_TOKEN

generate_post_data()
{
  cat <<EOF
{
  "tag_name": "$version",
  "target_commitish": "$branch",
  "name": "$version",
  "body": "",
  "draft": false,
  "prerelease": false
}
EOF
}

echo "Create release $version for repo: $repo_full_name branch: $branch"
curl -X POST "https://api.github.com/repos/$owner/$repo/releases" \
    -H "Authorization: token $token" \
    -H "owner: $owner" \
    -H "repo: $repo" \
    -H "accept: application/vnd.github+json" \
    --data "$(generate_post_data)"
