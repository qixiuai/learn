cc_binary(
    name = "hello_tf",
    srcs = ["hello_tf.c"],
    deps = [":libtensorflow"],
)

cc_binary(
    name = "tf_model",
    srcs = ["model.cc", "model.h"],
    deps = [":libtensorflow"],
)

cc_library(
    name = "libtensorflow",
    hdrs = glob(["include/**/*.h"]),
    includes = ["include"],
    deps = [":libtensorflow_", ":libtensorflow_framework"],
)

cc_import(
    name = "libtensorflow_",
    shared_library = "lib/libtensorflow.so",
)

cc_import(
    name = "libtensorflow_framework",
    shared_library = "lib/libtensorflow_framework.so",
)
