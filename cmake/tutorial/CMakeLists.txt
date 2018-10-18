cmake_minimum_required(VERSION 2.6)

project(Tutorial)
set(Tutorial_VERSION_MAJOR 1)
set(Tutorial_VERSION_MINOR 0)

configure_file(
  "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
  "${PROJECT_BINARY_DIR}/TutorialConfig.h"
  )

include_directories("${PROJECT_BINARY_DIR}")
include_directories("${PROJECT_SOURCE_DIR}/MathFunctions")
add_subdirectory(MathFunctions)

add_library(MathFunctions mysqrt.cxx)
add_executable(Tutorial tutorial.cxx)
target_link_libraries(Tutorial MathFunctions)

