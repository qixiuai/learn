package(
    default_visibility = ["//visibility:public"],
)

licenses(["notice"])


cc_library(
    name = "math",
    hdrs = ["math.h"],
    includes = ["."],
    deps = ["math_raw_lib"],
)

cc_import(
    name = "math_raw_lib",
    hdrs = ["math.h"],
    shared_library = "libmath.so",
)
