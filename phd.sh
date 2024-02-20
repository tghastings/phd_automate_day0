#!/bin/bash

# $1 is the GitHub Token
# $2 is the Repo URL 
echo $1
echo $2
docker run -e GITHUB_AUTH_TOKEN=$1 gcr.io/openssf/scorecard:stable --show-details --repo=https://$2 --checks Branch-Protection,Code-Review,Contributors,Maintained,Dangerous-Workflow,SAST,Vulnerabilities,Signed-Releases | grep Aggregate > tmp.txt
sed -i 's/Aggregate score: \([0-9]*\(\.[0-9]*\)\?\) \/ 10/\1/g' tmp.txt

/usr/bin/python3 ./dependents.py $2