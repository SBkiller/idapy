# -*- coding: utf-8 -*-

"""
"""

import os
import inspect

import idc
import idaapi
import idautils

import xrk_log


# ---------------------------------------------------------------------------
py_file_path = os.path.abspath(inspect.getsourcefile(lambda: 0))


# ---------------------------------------------------------------------------
v_log_header = "[XRK-EXPORT] >> "


def msg(str_):
    xrk_log.msg(v_log_header, str_)


# ---------------------------------------------------------------------------
def get_non_sub_functions(is_offset=False):
    """
        @param: is_offset : bool : is export offset or address

        @return: list : a list of tuple, each item: (start, end, name)
    """
    image_base = idaapi.get_imagebase()

    ret = []
    for f in idautils.Functions():
        name = idc.GetFunctionName(f)
        if not name.startswith("sub_") and not name.startswith("unknown"):

            start = idc.GetFunctionAttr(f, 0)
            end = idc.GetFunctionAttr(f, 4)
            if is_offset:
                start = start - image_base
                end = end - image_base

            ret.append((start, end, name))

    return ret


def save_non_sub_function(file_name, is_offset=False, is_hex=False):
    """
        @param: file_name : string : export file name
        @param: is_offset : bool   : is export offset or direct address
        @param: is_hex    : bool   : is export "value" as hex or int
    """
    f = open(file_name, "w")
    for func in get_non_sub_functions(is_offset=is_offset):

        if is_hex:
            f.write("%.8X %.8X %s\n" % (func[0], func[1], func[2]))
        else:
            f.write("%d %d %s\n" % (func[0], func[1], func[2]))
    f.close()
    # print "save non sub functio to file finish: %s" % file_name


# ---------------------------------------------------------------------------
if __name__ == "__main__":

    """
    # export for Immuntiy Debugger
    import xrk_util
    output_file = xrk_util.gen_path_in_idb_dir("1111_ida_names.txt")
    if output_file is not None:
        save_non_sub_function(output_file)
        msg("xrkexport for immunity debugger, finish: %s" % output_file)
    else:
        msg("xrkexport immunity debugger, no idb loaded")
    """

    # export for xrkpydbg
    output_file = idc.GetIdbPath().strip(".idb") + ".dll.txt"
    if os.path.exists(output_file):
        msg("can't export, file already exists: %s" % output_file)

    elif output_file is not None:
        save_non_sub_function(output_file, is_offset=True, is_hex=True)
        msg("xrkexport for xrkpydbg, finish: %s" % output_file)

    else:
        msg("xrkexport for xrkpydbg, no idb loaded")
