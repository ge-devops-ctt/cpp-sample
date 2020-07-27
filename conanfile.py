from conans import ConanFile, tools, CMake
import os

def getAppName():
    return os.getenv("GIT_REPO_NAME", "CppSample")

def coverage():
    return bool(os.getenv("ENABLE_COVERAGE", '0') == '1')

def coverityScan():
    return bool(os.getenv("COVERITY_SCAN", '0') == '1')


def getVersion():
    return os.getenv("VERSION", '0.1.0')

class TinyCSPLogConan(ConanFile):

    name = getAppName()
    version = getVersion()
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
