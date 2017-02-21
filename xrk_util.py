# -*- coding: utf-8 -*-

"""
"""

import os
import idc
import time


# ---------------------------------------------------------------------------
def time_str():
    """
        time string in this format: xx

        @return: STRING :
    """
    return time.strftime('%Y%m%d_%H_%M_%S', time.localtime(time.time()))


# ---------------------------------------------------------------------------
def get_idb_file_path():
    """
        TODO: there should be another better approach
    """
    # idaapi.get_input_file_path(): this return original path of idb file, even if file is copied to another directory
    file_path = idc.GetIdbPath()
    if file_path is None or len(file_path) == 0:
        return None
    return os.path.dirname(file_path)


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
