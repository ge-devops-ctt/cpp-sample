# docker run -it -w /app -v "C:\Users\212782121\Dev\devops\gitlab\GoogleTest-sample:/app" conanio/gcc8 bash
# export http_proxy=http://PITC-Zscaler-EMEA-Amsterdam3PR.proxy.corporate.ge.com:80
# export https_proxy=http://PITC-Zscaler-EMEA-Amsterdam3PR.proxy.corporate.ge.com:80

# docker exec -it testApplication bash
set -xe

if [ -z $1 ]
then
    export profile=profiles/x86_64;
else
    export profile=$1;
fi

export buildPath=build/
export sourcePath=src/
export ORG_NAME=CBT
ORG_NAME=${ORG_NAME:=GE-REN-GA-DevOps}
CHANNEL=${CHANNEL:=stable}

rm -r ${buildPath} || true
conan install . --install-folder=${buildPath} --profile ${profile} -u --build missing
conan build . --build-folder=${buildPath}
conan export-pkg . ${ORG_NAME}/${CHANNEL} --source-folder=${sourcePath} --build-folder=${buildPath} --force

set +x
