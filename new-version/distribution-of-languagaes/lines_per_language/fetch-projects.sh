#!/bin/sh
#
# Fetch the identified repo sample

# Fail on command errors and unset variables
set -eu

DATA_LOCATION=$(pwd)
REPO_LOCATION=$(pwd)

cat projects-accepted.txt |
while read name ; do
  grep -qx $name $DATA_LOCATION/projects-fetched.txt && continue
  dir_name=$REPO_LOCATION/$name
  if [ -d $dir_name ] ; then
    # Already there; refresh
    echo Refreshing $name 1>&2
    cd $dir_name
    default_branch=$(git remote show origin | grep 'HEAD branch' | cut -d\  -f5)
    git fetch origin $default_branch
  else
    cd $REPO_LOCATION
    user_name=$(dirname $name)
    mkdir -p $user_name
    cd $user_name
    #use regular git clone instead of --bare to analyze each repo code
    git clone --single-branch https://github.com/$name $(basename $name)
  fi
  echo $name >>$DATA_LOCATION/projects-fetched.txt
done
