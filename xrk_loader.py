# -*- coding: utf-8 -*

"""
0. 整合其他脚本

1. 各种导出，跟调试器配合使用

2. 动态解析出来的函数，设置其参数类型，之类的

3.
"""

import idaapi

import os
import sys
import inspect
file_path = os.path.abspath(inspect.getsourcefile(lambda: 0))
file_dir = os.path.dirname(inspect.getsourcefile(lambda: 0))

# 要在这里插入path，不然弹出的界面没有图标
sys.path.insert(0, os.path.join(file_dir, "xrk_pyeditor\\icons"))
from ico import *


#
# 避免重新打开IDA来加载修改后的py文件的方式：
# 用固定的py文件，注册功能，在功能代码中调用：idaapi.IDAPython_ExecScript()
#


#
# 可用的快捷键：
# Alt-N
# Alt-Z
# Ctrl-H
# Ctrl-Y
#

# ---------------------------------------------------------------------------
v_log_header = "[XRK-LOADER] >> "


def msg(str_):
    idaapi.msg("%s%s\n" % (v_log_header, str_))


def msgs(strs):
    for str_ in strs:
        msg(str_)


def warn(str_):
    idaapi.msg("%s%s\n" % (v_log_header, str_))


# ---------------------------------------------------------------------------
class handler_test(idaapi.action_handler_t):
    def __init__(self):
        idaapi.action_handler_t.__init__(self)

    def activate(self, ctx):
        """
            @param: ctx : obj : idaapi.action_activation_ctx_t()
        """
        msg("hander test -- activate")

    def update(self, ctx):
        """
            @param: ctx : obj : idaapi.action_update_ctx_t()

            @return: int : idaapi.AST_XX(enum action_state_t{})
        """
        msg("hander test -- update")
        return idaapi.AST_ENABLE_ALWAYS


class handler_pt_list(idaapi.action_handler_t):
    def __init__(self):
        idaapi.action_handler_t.__init__(self)

    def activate(self, ctx):
        lines = []
        lines.append("Ctrl + Alt + 0  >> print registered script file list")
        lines.append("Ctrl + Alt + 1  >> test")
        lines.append("Ctrl + Alt + 2  >> pop script editor window")
        msgs(lines)

    def update(self, ctx):
        return idaapi.AST_ENABLE_ALWAYS


class handler_py_editor(idaapi.action_handler_t):
    def __init__(self):
        idaapi.action_handler_t.__init__(self)

    def activate(self, ctx):
        """
            exec script to pop up python editor window
        """
        g = globals()
        idaapi.IDAPython_ExecScript(os.path.join(file_dir, "xrk_pyeditor\\pyeditor.py"), g)

    def update(self, ctx):
        return idaapi.AST_ENABLE_ALWAYS


class handler_exec_py_script(idaapi.action_handler_t):
    def __init__(self, py_script_name):
        """
            store python file path
        """
        idaapi.action_handler_t.__init__(self)
        self.py_script_path = os.path.join(file_dir, py_script_name)

        if not os.path.exists(self.py_script_path):
            warn("python script file not exists: %s" % self.py_script_path)

    def activate(self, ctx):
        """
            execute script
        """
        if not os.path.exists(self.py_script_path):
            warn("python script file not exists: %s" % self.py_script_path)
        else:
            g = globals()
            idaapi.IDAPython_ExecScript(self.py_script_path, g)

    def update(self, ctx):
        """
            TODO: update @return accordingly.
        """
        return idaapi.AST_ENABLE_ALWAYS


# ---------------------------------------------------------------------------
class xrkloader(idaapi.plugin_t):

    flags = idaapi.PLUGIN_FIX
    comment = "This is loader for many scripts"

    help = "register many shortcuts to execute standalone python scripts"
    wanted_name = "xrkloader"
    wanted_hotkey = "ALT-N"

    def init(self):
        # msg("init()")
        return idaapi.PLUGIN_OK

    def run(self, arg):
        # msg("run()")
        idaapi.register_action(idaapi.action_desc_t("print script list", "print script list", handler_pt_list(), "Ctrl-Alt-0", "print script list(with shortcuts)"))
        idaapi.register_action(idaapi.action_desc_t("name-test", "label-test", handler_test(), "Ctrl-Alt-1", "just test for xrk loader"))
        idaapi.register_action(idaapi.action_desc_t("py_editor", "py_editor", handler_exec_py_script("xrk_pyeditor\\pyeditor.py"), "Ctrl-Alt-2", "python script editor"))
        idaapi.register_action(idaapi.action_desc_t("unexp_walk", "unexp_walk", handler_exec_py_script("xrk_unexp_walk.py"), "Ctrl-Alt-3", "walk to next unexplorered code"))
        idaapi.register_action(idaapi.action_desc_t("auto_rename", "auto_rename", handler_exec_py_script("xrk_auto_re.py"), "Ctrl-Alt-4", "auto rename some functions"))
        # msg("run() -- finish")

    def term(self):
        # msg("term()")
        pass


# ---------------------------------------------------------------------------
def PLUGIN_ENTRY():
    return xrkloader()
