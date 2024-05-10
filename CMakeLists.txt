cmake_minimum_required(VERSION 3.14)
set(CMAKE_CXX_STANDARD 17)

project(doozer LANGUAGES C CXX)

set(CMAKE_VERBOSE_MAKEFILE ON)

find_package(
  Python
  COMPONENTS Interpreter Development.Module
  REQUIRED
  )

  message(STATUS "Python: " ${Python_EXECUTABLE})
include_directories(${NUMPY_INCLUDE})


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
