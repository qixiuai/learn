cmake_minimum_required(VERSION 3.13)

project (Example)

add_subdirectory(MathFunctions)
include_directories("$(PROJECT_SOURCE_DIR)/MathFunctions")

add_executable(Example example.cc)
target_link_libraries(Example MathFunctions)






