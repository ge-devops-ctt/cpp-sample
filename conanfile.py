from conans import ConanFile, tools, CMake
import os

def getAppName():
    return os.getenv("GIT_REPO_NAME", "GoogleTest Sample")

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

        cmake = CMake(self)
        cmake.configure(source_folder="src")
        cmake.build()
