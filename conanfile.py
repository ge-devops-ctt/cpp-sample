from conans import ConanFile, tools, CMake
import os

def getAppName():
    return os.getenv("GIT_REPO_NAME", "GoogleTest Sample")

def coverage():
    return bool(os.getenv("ENABLE_COVERAGE", '0') == '1')

def coverityScan():
    return bool(os.getenv("COVERITY_SCAN", '0') == '1')

class TinyCSPLogConan(ConanFile):

    name = getAppName()
    version = "0.1.0"
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
