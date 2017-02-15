import idaapi

# from inspect import getsourcefile
# from os.path import abspath
# abspath(getsourcefile(lambda: 0)) ==> F:\SVN\ida\xrk_pytest.py


class xrkpytest(idaapi.plugin_t):

    flags = idaapi.PLUGIN_FIX
    comment = "This is a just test plugin"

    help = "xrkpytest"
    wanted_name = "xrkpytest"
    wanted_hotkey = ""

    def init(self):
        idaapi.msg("xrkpytest -- init()\n")
        return idaapi.PLUGIN_OK

    def run(self, arg):
        idaapi.msg("xrkpytest -- run()\n")

    def term(self):
        idaapi.msg("xrkpytest -- term()\n")


def PLUGIN_ENTRY():
    return xrkpytest()
