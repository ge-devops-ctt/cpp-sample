cmake_minimum_required(VERSION 3.10.0)
project(CppSample)
set(CMAKE_VERBOSE_MAKEFILE ON)

# C++ configuration

if(CMAKE_HOST_SYSTEM_NAME STREQUAL  "Windows" OR CMAKE_HOST_SYSTEM_NAME STREQUAL  "Linux")
    set(CMAKE_CXX_STANDARD 11)
    set(CMAKE_CXX_STANDARD_REQUIRED True)
else()
    set(CMAKE_CXX_STANDARD 98)
    set(CMAKE_CXX_STANDARD_REQUIRED True)
endif()
# Setup Target flags
if(CMAKE_HOST_SYSTEM_NAME STREQUAL  "Windows")
    message("  * Windows Is detected will add -DWIN32 ")
    add_definitions(-DWIN32)
elseif(CMAKE_HOST_SYSTEM_NAME STREQUAL  "Linux")
    message("  * Linux Is detected will add -D__unix__ ")
    add_definitions(-D__unix__ -DUNIX)
endif()

# setup conan
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# Configure project level include directories
include_directories(${CONAN_INCLUDE_DIRS})
include_directories(${CMAKE_SOURCE_DIR}/app)

# Configure project Link directories
link_directories(${CONAN_LIB_DIRS})

add_subdirectory(app)

#enable_testing()
#add_subdirectory(test)

