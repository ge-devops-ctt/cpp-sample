# docker exec -it testApplication bash
set -x

if [ -z $1 ]
then
    export profile=profiles/x86_64;
else
    export profile=$1;
fi

export buildPath=build/
export sourcePath=src/
export ORG_NAME=CBT
export CHANNEL=stable

rm -r ${buildPath}
conan install . --install-folder=${buildPath} --profile ${profile} -u
conan build . --build-folder=${buildPath}
#conan export-pkg . ${ORG_NAME}/${CHANNEL} --source-folder=${sourcePath} --build-folder=${buildPath} --force
#ls

set +x
