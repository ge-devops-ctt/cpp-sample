cmake_minimum_required(VERSION 3.10.0)
project(Factorial)

# setup conan
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
 
set(SRC_FOLDER ${CMAKE_CURRENT_SOURCE_DIR}/*.cc ${CMAKE_CURRENT_SOURCE_DIR}/*.h)
file(GLOB_RECURSE SRC_FILES ${SRC_FOLDER})
 
link_directories(${CONAN_LIB_DIRS})

add_library(factorial SHARED ${SRC_FILES})
 
