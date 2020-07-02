conan config set proxies.http=http://PITC-Zscaler-EMEA-Amsterdam3PR.proxy.corporate.ge.com:80
conan config set proxies.https=http://PITC-Zscaler-EMEA-Amsterdam3PR.proxy.corporate.ge.com:80
conan config set proxies.no_proxy_match=https://artifactory.build.ge.com*
conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan False
conan remote update conan-center https://conan.bintray.com False

conan remote add DYIYM https://artifactory.build.ge.com/api/conan/DYIYM False
conan user -p s0ftwar3CBT -r DYIYM 502811516
conan remote add DYIYM-SNAPSHOT https://artifactory.build.ge.com/api/conan/DYIYM-SNAPSHOT False
conan user -p s0ftwar3CBT -r DYIYM-SNAPSHOT 502811516