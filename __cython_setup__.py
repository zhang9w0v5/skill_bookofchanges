# -*-  coding: UTF-8  -*-
# -*- -*- -*- -*- -*- -*-
# 2023/03    zhang9w0v5    created
# 2024/04    zhang9w0v5    upgrade
# -*- -*- -*- -*- -*- -*-
from setuptools import setup
from Cython.Build import cythonize
# -*- -*- -*- -*- -*- -*-
setup(
    name='Book Of Changes',
    ext_modules=cythonize([
        "bookofchanges.py"
    ]),
    compiler_directives={
        "language_level"        : 3,        # 指定语言级别（Python2或3）
        "cdivision"             : True,     # 启用C风格除法（利于生成更接近底层C语言的代码）
        "linetrace"             : False,    # 禁用行号跟踪（影响代码覆盖率）
        "profile"               : False,    # 禁用性能分析
        "boundscheck"           : False,    # 禁用边界检查（利于生成更接近底层C语言的代码）
        "wraparound"            : False,    # 禁用负数索引（利于生成更接近底层C语言的代码）
        "nonecheck"             : False,    # 禁用None检查（利于生成更接近底层C语言的代码）
        "embedsignature"        : False,    # 禁用嵌入函数签名
        "overflowcheck"         : False,    # 禁用溢出检查
        "warn.undeclared"       : False,    # 禁用未声明变量警告
        "warn.unused"           : False,    # 禁用未使用变量警告
        "warn.redundant"        : False,    # 禁用冗余赋值警告
        "warn.unreachable"      : False,    # 禁用不可达代码警告
        "warn.unused_result"    : False,    # 禁用未使用返回值警告
        "warn.unused_arg"       : False,    # 禁用未使用参数警告
        "warn.unused_clsarg"    : False,    # 禁用未使用类参数警告
        "warn.unused_element"   : False,    # 禁用未使用元素警告
        "warn.unused_variable"  : False,    # 禁用未使用变量警告
    },
    define_macros      = [('CYTHON_TRACE', '0')],    # 禁用Cython跟踪（相当于linetrace=False）
    extra_compile_args = ['-O2', '-DNDEBUG'],        # 编译器优化选项，移除调试信息
    extra_link_args    = ['-O2']                     # 链接器优化选项
)
# -*- -*- -*- -*- -*- -*-
