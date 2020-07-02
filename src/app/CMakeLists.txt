cmake_minimum_required(VERSION 3.10.0)
project(GoogleTests)

set(BINARY GoogleTests)
 
set(SRC_FOLDER ${PROJECT_PATH}/*.cc)
file(GLOB_RECURSE SRC_FILES ${SRC_FOLDER})
 
link_directories(${CONAN_LIB_DIRS})

add_executable(factorial-bin ${SRC_FILES})
add_library(factorial SHARED ${SRC_FILES})
 
