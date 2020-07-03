cmake_minimum_required(VERSION 3.10.0)
project(GoogleTests)

# setup conan
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()


set(BINARY GoogleTests)
 
set(SRC_FOLDER ${PROJECT_PATH}/*.cc)
file(GLOB_RECURSE SRC_FILES ${SRC_FOLDER})
 
link_directories(${CONAN_LIB_DIRS})

add_library(factorial SHARED ${SRC_FILES})
 
