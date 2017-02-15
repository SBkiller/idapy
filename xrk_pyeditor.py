# Created by: Storm Shadow http://www.techbliss.org

# WARNING! All changes made in this file will be lost!
# import re
import idaapi
# import idc
from idc import *
from idaapi import *
import sys

import os
import inspect
file_path = os.path.dirname(inspect.getsourcefile(lambda: 0))
sys.path.insert(0, os.path.join(file_path, "xrk_pyeditor\\icons"))
from ico import *


#
# we need 2 "ALT-E" to make editor window popup.
# 1. register menu item with shortcut
# 2. trigger shortcut to popup editor window
#
# todo: what about self.popeye() in self.run() directly instead of register menu item?
#


class ripeye(idaapi.plugin_t):
    flags = idaapi.PLUGIN_FIX
    comment = "This is a comment"

    help = "Python Editor"
    wanted_name = "Python Editor"
    wanted_hotkey = "ALT-E"

    def init(self):
        idaapi.msg("Python Editor Is Found Use ALT+E to load to menu \n")
        return idaapi.PLUGIN_OK

    # def run(self, arg):
    #     idaapi.msg("run() called with %d!\n" % arg)

    def term(self):
        idaapi.msg("")

    def AddMenuElements(self):
        idaapi.add_menu_item("File/", "Code editor", "ALT-E", 0, self.popeye, ())
        idaapi.set_menu_item_icon("File/Code editor", idaapi.load_custom_icon(":/ico/python.png"))

    def run(self, arg=0):
        idaapi.msg("Python Editor Loaded to menu use ALT+E once more")
        self.AddMenuElements()

    def popeye(self):
        g = globals()
        IDAPython_ExecScript(os.path.join(file_path, "xrk_pyeditor\\pyeditor.py"), g)


def PLUGIN_ENTRY():
    return ripeye()
