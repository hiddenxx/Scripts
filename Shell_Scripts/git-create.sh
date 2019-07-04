#!/bin/sh

repo_name=$1
github_username=hiddenxx

if [[ ! -e $repo_name ]]; then
    mkdir $repo_name
elif [[ ! -d $repo_name ]]; then
    echo "$repo_name already exists but is not a directory" 1>&2
fi

cd $repo_name
git init
git add . && git commit -m "First Commit"

test -z $repo_name && echo "Repo name required." 1>&2 && exit 1

curl -u $github_username https://api.github.com/user/repos -d "{\"name\":\"$repo_name\"}"

git remote add origin "https://github.com/$github_username/$repo_name.git"
