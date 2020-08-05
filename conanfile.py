from conans import ConanFile, tools, CMake
import os
#import semver
from git import Repo

# Manage semver du to conflict with a Conan dependency
import importlib.util
spec = importlib.util.spec_from_file_location("semver", "/opt/pyenv/versions/3.7.5/lib/python3.7/site-packages/semver.py")
semver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(semver)

# dir_path = os.path.abspath(".")
dir_path = os.getenv("CI_PROJECT_DIR", "/app")
print(dir_path)
repo = Repo(dir_path)


def latest_tag():
    try:
        tag = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)[-1]
    except:
        tag = "1.0.0"

    return str(tag)

def get_version():
    branch = os.getenv("CI_COMMIT_REF_NAME") if "CI_COMMIT_REF_NAME" in os.environ else repo.head.reference.name
    tag = latest_tag()
    print(tag)
    next_tag = semver.VersionInfo.parse(tag).bump_minor()
    print(next_tag)
    new_tag = os.getenv("CI_COMMIT_TAG")
    if new_tag:
        version = new_tag
    elif branch == "master":
        version = next_tag.bump_prerelease()
    else:
        version = f"{next_tag}-{branch}"

    return version

def getAppName():
    return os.getenv("GIT_REPO_NAME", "CppSample")

def coverage():
    return bool(os.getenv("ENABLE_COVERAGE", '0') == '1')

def coverityScan():
    return bool(os.getenv("COVERITY_SCAN", '0') == '1')




class TinyCSPLogConan(ConanFile):

    name = getAppName()
    version = get_version()
    url = "None"
    license = "None"
    description = "Google test sample"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": True}
    generators = "cmake"
    exports_sources = "src/*"


    def requirements(self):
        self.requires("gtest/1.8.1@bincrafters/stable")

    def build(self):
        if coverage():
            cmake = CMake(self, build_type='Debug')
            cmake.configure(source_folder="src")
            cmake.build()
            cmake.test()
            cmake.build(target='gcovr')
        else:
            cmake = CMake(self)
            cmake.configure(source_folder="src")
            if coverityScan():
                self.run("cov-configure --gcc")
                self.run("cov-build --dir covtemp cmake --build .")
                self.run("cov-analyze --dir covtemp --all --export-summaries=false")
            else:
                cmake.build()
    
    def package(self):
        self.copy("*.h", dst="include", src="src/app/", keep_path=False)

        if (self.settings.os == "Windows"):
            if self.options.shared:
                self.copy("*.dll", dst="bin", src="bin", keep_path=False)

        if (self.settings.os == "Linux"):
            if self.options.shared:
                self.copy("*.so", dst="lib", src="app/lib", keep_path=False)
            else:
                self.copy("*.a", dst="lib", src="app/lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs = [
            "include",
        ]
        self.cpp_info.resdirs = ['res']
