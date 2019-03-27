cc_binary(
    name = "math.dll",
    srcs = ["math.cc", "math.h"],
    copts = ["-std=c++17"],
    features = ["windows_export_all_symbols"],
    linkshared = 1,
)


cc_library(
    name = "math",
    srcs = ["math.cc", "math.h"],
    hdrs = ["math.h"],
    copts = ["-std=c++17"],
)
