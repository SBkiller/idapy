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

def cbk_filter_not_sub_nor_unknown(f):
    """
        @param: f : function obj

        @return: list : a list of tuple, each item: (start, end, name)
    """
    name = idc.GetFunctionName(f)
    return not name.startswith("sub_") and not name.startswith("unknown")


def _get_func(is_offset=False, cbk_filter=None):
    """
        @param: is_offset  : bool   : (optional, dft=Flase)is export offset or address
        @param: cbk_filter : method : prototype: bool cbk_filter(func)

        @return: list : a list of tuple, each item: (start, end, name)
    """
    image_base = idaapi.get_imagebase()

    ret = []
    for f in idautils.Functions():

        if cbk_filter is not None and not cbk_filter(f):
            continue

        name = idc.GetFunctionName(f)
        start = idc.GetFunctionAttr(f, 0)
        end = idc.GetFunctionAttr(f, 4)
        if is_offset:
            start = start - image_base
            end = end - image_base

        ret.append((start, end, name))

    return ret


def _save_func(file_name, is_offset=False, is_hex=False, cbk_filter=None):
    """
        @param: file_name  : string : export file name
        @param: is_offset  : bool   : is export offset or direct address
        @param: is_hex     : bool   : is export "value" as hex or int
        @param: cbk_filter : method : prototype: bool cbk_filter(func)
    """
    try:
        f = open(file_name, "w")
    except:
        print "open file exception: %s" % file_name
    else:
        for func in _get_func(is_offset=is_offset, cbk_filter=cbk_filter):

            if is_hex:
                f.write("%.8X %.8X %s\n" % (func[0], func[1], func[2]))
            else:
                f.write("%d %d %s\n" % (func[0], func[1], func[2]))
        f.close()
        # print "func infos saved to: %s" % file_name


# ---------------------------------------------------------------------------
if __name__ == "__main__":

    # export non sub function and function range for Immuntiy Debugger
    # import xrk_util
    # output_file = xrk_util.gen_path_in_idb_dir("1111_ida_names.txt")
    # if output_file is not None:
    #     _save_func(output_file, is_offset=True, is_hex=True, cbk_filter=cbk_filter_not_sub_nor_unknown)
    #     msg("xrkexport for immunity debugger, finish: %s" % output_file)
    # else:
    #     msg("xrkexport immunity debugger, no idb loaded")

    # export non sub function and function range for xrkpydbg
    # output_file = idc.GetIdbPath().strip(".idb") + ".dll.txt"
    # if os.path.exists(output_file):
    #     msg("can't export, file already exists: %s" % output_file)
    # elif output_file is not None:
    #     _save_func(output_file, is_offset=True, is_hex=True, cbk_filter=cbk_filter_not_sub_nor_unknown)
    #     msg("xrkexport for xrkpydbg, finish: %s" % output_file)
    # else:
    #     msg("xrkexport for xrkpydbg, no idb loaded")

    # export function address for xrkpydbg
    import xrk_util
    output_file = xrk_util.gen_path_in_idb_dir("1111_ida_funcs.txt")
    if output_file is not None:
        _save_func(output_file, is_offset=False, is_hex=True, cbk_filter=None)
    else:
        msg("export function address, no idb loaded")
