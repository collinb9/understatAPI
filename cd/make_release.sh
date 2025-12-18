#!/usr/bin/env sh

set -e

version=$1
branch=master
repo=understatapi
owner=collinb9
token=$GITHUB_TOKEN
changeLog=`git log $(git tag -l | grep -v 'b' | tail -n 1)..HEAD --oneline --no-decorate --no-abbrev-commit | sed 's/\r$//'`

generate_post_data()
{
  jq -n \
    --arg version "$version" \
    --arg branch "$branch" \
    --arg body "Commits since last release:\n$changeLog" \
    '{
      "tag_name": $version,
      "target_commitish": $branch,
      "name": $version,
      "body": $body,
      "draft": false,
      "prerelease": false
    }'
}

# Validate JSON before sending
generate_post_data | jq -e . >/dev/null

echo "Create release $version for repo: $repo_full_name branch: $branch"
curl -X POST "https://api.github.com/repos/$owner/$repo/releases" \
    -H "Authorization: token $token" \
    -H "owner: $owner" \
    -H "repo: $repo" \
    -H "accept: application/vnd.github+json" \
    --data-binary "$(generate_post_data)"
