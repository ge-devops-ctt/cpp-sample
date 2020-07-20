cmake_minimum_required(VERSION 3.10.0)
project(GoogleTests)

# setup conan
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()



# Add code coverage
if (CMAKE_BUILD_TYPE STREQUAL "Debug")
    message("Code Coverage enabled")
    # Set OBJECT_DIR to the objects output directory of your project
    set(OBJECT_DIR ${CMAKE_BINARY_DIR}/test/CMakeFiles/GoogleTests.dir/)
    # Exclude header files
    set(REG "'.*\\.h'")
    message(${REG})
    message( ${OBJECT_DIR} )
    # add definitions
    add_definitions(-fprofile-arcs -ftest-coverage)
    # Set the compiler options
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -g -O0 -Wall -fprofile-arcs -ftest-coverage")
    set(CMAKE_CXX_OUTPUT_EXTENSION_REPLACE ON)
    # Create the gcov target. Run coverage tests with 'make gcov'
    add_custom_target(gcovr
        #COMMAND ${CMAKE_MAKE_PROGRAM} test
        #COMMAND mkdir -p "${CMAKE_BINARY_DIR}/coverage/"
        COMMAND gcovr 
        -r "${CMAKE_SOURCE_DIR}/app"
        --object-directory "${OBJECT_DIR}"
        --gcov-executable "/usr/bin/gcov-8"
        -e ${REG}
        COMMAND gcovr 
        -r "${CMAKE_SOURCE_DIR}/app"
        --object-directory "${OBJECT_DIR}"
        --gcov-executable "/usr/bin/gcov-8"
        -e ${REG}
        --xml
        -o "${CMAKE_BINARY_DIR}/cobertura-coverage.xml"
         COMMAND gcovr 
        #-r "${CMAKE_SOURCE_DIR}/app"
        -r "${CMAKE_SOURCE_DIR}/.."
        --object-directory "${OBJECT_DIR}"
        --gcov-executable "/usr/bin/gcov-8"
        -e ${REG}
        --exclude-directories "${CMAKE_SOURCE_DIR}/test/"
        --sonarqube
        -o "${CMAKE_BINARY_DIR}/sonar-coverage.xml"
        )
endif ()

#set(SRC_FOLDER ${SRC_PROJECT_PATH}/src/*.cc)
#file(GLOB_RECURSE SRC_FILES ${SRC_FOLDER})

 
set(BINARY GoogleTests)
message("--------------------------${CMAKE_CURRENT_SOURCE_DIR}/*.cc ---------------------")
set(SRC_FOLDER ${CMAKE_CURRENT_SOURCE_DIR}/*.cc)
file(GLOB_RECURSE SRC_FILES ${SRC_FOLDER})
message("--------------------------${CMAKE_SOURCE_DIR}/app/*.cc ---------------------")
set(SRC_PROJECT_FOLDER ${CMAKE_SOURCE_DIR}/app/*.cc)
file(GLOB_RECURSE SRC_PROJECT_FILES ${SRC_PROJECT_FOLDER})

set(SRC_PROJECT_HEADERS_FOLDER ${CMAKE_SOURCE_DIR}/app/*.h)
file(GLOB_RECURSE SRC_PROJECT_HEADERS ${SRC_PROJECT_HEADERS_FOLDER})

include_directories(${CMAKE_SOURCE_DIR}/app)

link_directories(${CONAN_LIB_DIRS})

add_executable(${BINARY} ${SRC_FILES} ${SRC_PROJECT_FILES} ${SRC_PROJECT_HEADERS})

target_link_libraries(${BINARY} ${CONAN_LIBS})

set_target_properties(GoogleTests PROPERTIES LINKER_LANGUAGE CXX)

add_test(NAME ${BINARY} COMMAND ${BINARY})


