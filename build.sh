# docker run -it -w /app -v "C:\Users\212782121\Dev\devops\gitlab\GoogleTest-sample:/app" conanio/gcc8 bash
# export http_proxy=http://PITC-Zscaler-EMEA-Amsterdam3PR.proxy.corporate.ge.com:80
# export https_proxy=http://PITC-Zscaler-EMEA-Amsterdam3PR.proxy.corporate.ge.com:80

# docker exec -it testApplication bash
set -xe

PROFILE=${PROFILE:=profiles/x86_64}
BUILD_PATH=${BUILD_PATH:==build}
SOURCE_PATH=${SOURCE_PATH:==src}
ORG_NAME=${ORG_NAME:=GE-REN-GA-DevOps}
CHANNEL=${CHANNEL:=stable}

rm -r ${BUILD_PATH} || true
conan install . --install-folder=${BUILD_PATH} --profile ${PROFILE} -u --build missing
conan build . --build-folder=${BUILD_PATH}
conan export-pkg . ${ORG_NAME}/${CHANNEL} --source-folder=${SOURCE_PATH} --build-folder=${BUILD_PATH} --force

set +x
