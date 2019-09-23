# *-* python *-*

def clean_dep(dep):
    return str(Label(dep))

def if_linux_x86_64(a, other_wise=[]):
    return select({
        clean_dep("//tensorflow:linux_x86_64"): a,
        "//conditions:default": other_wise,
    })


def get_win_copts(is_external = False):
    return []

def tf_copts(is_external = False):
    copts = [
        "-std=c++17",
    ]
    return copts

def tf_gen_op_libs(op_lib_names, deps = None, is_external = True):
    if not deps:
        deps = []
    for n in op_lib_names:
        native.cc_library(
            name = n + "_op_lib",
            copts = tf_copts(is_external = is_external),
            srcs = ["ops/" + n + ".cc"],
            deps = deps + [clean_dep("//tensorflow/core:framework")],
            visibility = ["//visibility:public"],
            alwayslink = 1,
            linkstatic = 1,
        )

def _py_wrap_cc_impl(ctx):
    srcs = ctx.files.srcs
    if len(srcs) != 1:
        fail("Exactly one SWIG source file label must be specified.","srcs")
    module_name = ctx.attr.module_name
    src = ctx.files.srcs[0]
    inputs = []
    swig_include_dirs = []
    args = [
        "-c++",
        "-python",
        "-module",
        module_name,
        "-o",
        ctx.outputs.cc_out.path,
        "-outdir",
        ctx.outputs.py_out.dirname,
    ]
    outputs = []
    ctx.actions.run(
        executable = ctx.executable._swig,
        arguments = args,
        inputs = iputs,
        outputs = outputs,
        mnemonic = "PythonSwig",
        progress_message = "SWIGing" + src.path,
    )
    return struct(files = depset(outputs))



def tf_py_wrap_cc(
        name,
        srcs,
        swig_includes = [],
        deps = [],
        copts = [],
        **kwargs):
    module_name = name.split("/")[-1]
    cc_library_name = "/".join(name.split("/")[:-1] + ["_" + module_name + ".so"])
    cc_library_pyd_name = "/".join(
        name.split("/")[:-1] + ["_" + module_name + ".pyd"]
    )
    extra_deps = []
    _py_wrap_cc(
        name = name + "_py_wrap",
        srcs = srcs,
        module_name = module_name,
        py_module_name = name,
        swig_includes = swig_includes,
        toolchain_deps = ["@bazel_tools//tools/cpp:current_cc_toolchain"],
        deps = deps + extra_deps,
    )
    extra_linkopts = select({
        "@local_config_cuda//cuda:darwin": [
            "-Wl,-exported_symbols_list,$(location %s.lds)" % vscriptname,
        ]
        clean_dep("//tensorflow:windows"): [],
        "//conditions:default": [
            "-Wl,--version_script",
            "$(location %s.lds)" % vscriptname,
        ],
    })
    extra_deps += select({
        "@local_config_cuda//cuda:darwin": [
            "%s.lds" % vscriptname,
        ],
        clean_dep("//tensorflow:windows"): [],
        "//conditions:default": [
            "%s.lds" % vscriptname,
        ],
    })

    tf_cc_shared_object(
        name = cc_library_name,
        srcs = [moudle_name + ".cc"]
        copts = copts + if_not_windows([
            "-Wno-self-assign",
            "-Wno-sign-compare",
            "-Wno-write-strings",
        ])
        linkopts = extra_linkopts,
        linkstatic = 1,
        deps = deps + extra_deps,
        **kwargs,
    )
    native.genrule(
        name = "gen_" + cc_library_pyd_name,
        srcs = [":" + cc_library_name],
        outs = [cc_library_pyd_name],
        cmd = "cp $< $@",
    )
    native.py_library(
        name = name,
        srcs = [":" + name + ".py"],
        srcs_version = "PY3",
        data = select({
            clean_dep("//tensorflow:windows"): [":" + cc_library_pyd_name],
            "//conditions:default": [":" + cc_library_name],
        }),
    )
    

print(clean_dep("dep"))


