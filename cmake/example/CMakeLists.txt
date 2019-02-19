cmake_minimum_required (VERSION 2.6)
project (Example)
add_executable(Example example.cc)
add_library(Libexample SHARED STATIC example.cc)

