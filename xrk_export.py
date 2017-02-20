# -*- coding: utf-8 -*-

"""
"""

import os
import idc
import time
import idaapi
import inspect
import idautils


# ---------------------------------------------------------------------------
py_file_path = os.path.abspath(inspect.getsourcefile(lambda: 0))


def get_idb_file_path():
    """
        TODO: there should be another better approach
    """
    # idaapi.get_input_file_path(): this return original path of idb file, even if file is copied to another directory
    file_path = idc.GetIdbPath()
    if file_path is None or len(file_path) == 0:
        return None
    return os.path.dirname(file_path)


def time_str():
    """
        time string in this format: xx

        @return: STRING :
    """
    return time.strftime('%Y%m%d_%H_%M_%S', time.localtime(time.time()))


def gen_path_in_idb_dir(tail, add_time_prefix=True):
    """
    """
    idb_file_path = get_idb_file_path()
    if idb_file_path is None or len(idb_file_path) == 0:
        return None
    if add_time_prefix:
        return os.path.join(idb_file_path, time_str() + "_" + tail)
    return os.path.join(idb_file_path, tail)


# ---------------------------------------------------------------------------
v_log_header = "[XRK-EXPORT] >> "


def msg(str_):
    """
    """
    idaapi.msg("%s%s\n" % (v_log_header, str_))


# ---------------------------------------------------------------------------
def get_non_sub_functions():
    """
    """
    ret = []
    for f in idautils.Functions():
        name = idc.GetFunctionName(f)
        if not name.startswith("sub_") and not name.startswith("unknown"):
            ret.append((idc.GetFunctionAttr(f, 0), idc.GetFunctionAttr(f, 4), name))
    return ret


def save_non_sub_function(file_name):
    """
    """
    f = open(file_name, "w")
    for func in get_non_sub_functions():
        f.write("%d %d %s\n" % (func[0], func[1], func[2]))
    f.close()
    # print "save non sub functio to file finish: %s" % file_name


# ---------------------------------------------------------------------------
output_file = gen_path_in_idb_dir("1111_ida_names.txt")
if output_file is not None:
    save_non_sub_function(output_file)
    msg("xrkexport, finish")

else:
    msg("xrkexport, no idb loaded")
