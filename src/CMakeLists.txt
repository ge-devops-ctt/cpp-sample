cmake_minimum_required(VERSION 3.10.0)
project(GoogleTests)


# setup conan
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
 
set(BINARY GoogleTests)
 
file(GLOB_RECURSE TEST_SOURCES LIST_DIRECTORIES false *.h *.cc)
 
set(SOURCES ${TEST_SOURCES})
 
add_executable(${BINARY} ${TEST_SOURCES})
 
add_test(NAME ${BINARY} COMMAND ${BINARY})
link_directories(${CONAN_LIB_DIRS})
target_link_libraries(${BINARY} ${CONAN_LIBS})
