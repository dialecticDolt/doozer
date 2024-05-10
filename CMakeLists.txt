cmake_minimum_required(VERSION 3.14)
set(CMAKE_CXX_STANDARD 17)

project(${SKBUILD_PROJECT_NAME} LANGUAGES C CXX)

set(CMAKE_VERBOSE_MAKEFILE ON)

find_package(
  Python
  COMPONENTS Interpreter Development.Module
  REQUIRED
)

set(CYTHON cython)
message(STATUS "Cython: " ${CYTHON})
#Test if cython is installed
if(NOT CYTHON)
  message(
    FATAL_ERROR
      "Cython is required to build Parla. Please install cython and try again."
    )
endif()
#Test if cython exists
execute_process(COMMAND ${CYTHON} --version ERROR_QUIET OUTPUT_VARIABLE CYTHON_VERSION)
if(NOT CYTHON_VERSION)
  message(
    FATAL_ERROR
      "Cython is required to build Parla. Please install cython and try again."
    )
endif()

message(STATUS "Python: " ${Python_EXECUTABLE})
include_directories(${NUMPY_INCLUDE})

set(CYTHON_FLAGS "--cplus;--fast-fail")

set(3RD_PARTY_DIR ${PROJECT_SOURCE_DIR}/3rd-party)

if(DOOZER_ENABLE_NVTX)
    set(NVTX_INCLUDE ${3RD_PARTY_DIR}/nvtx/c/include)
endif(DOOZER_ENABLE_NVTX)

message(STATUS "Python3_EXECUTABLE: ${Python3_EXECUTABLE}")
message(STATUS "Python3_INCLUDE_DIRS: ${Python3_INCLUDE_DIRS}")
message(STATUS "Python3_LIBRARIES: ${Python3_LIBRARIES}")
message(STATUS "Python3_VERSION: ${Python3_VERSION}")
message(STATUS "Numpy Include: ${NUMPY_INCLUDE}")
message(STATUS "Numpy Include Directories : ${Python3_NumPy_INCLUDE_DIRS}")

#Compile C++ Implementation Source
add_subdirectory(src/doozer/impl)

#Compute Cython Wrapper
add_subdirectory(src/doozer)
