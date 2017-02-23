# -*- coding: utf-8 -*

"""
test module
"""

import os
import inspect

import idaapi
import xrk_log

file_path = os.path.abspath(inspect.getsourcefile(lambda: 0))
file_dir = os.path.dirname(inspect.getsourcefile(lambda: 0))

# ---------------------------------------------------------------------------
v_log_header = "[XRK-TEST] >>"


def msg(str_):
    xrk_log.msg(v_log_header, str_)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    msg("from hello")

    file_path = idaapi.askfile_c(0, "_api_summary.dat", "plese select api summary file")
    if os.path.exists(file_path):
        try:
            # file_path = r"E:\SVN\repo-pydbg\1111_api_summary.dat"
            file = open(file_path, "r")
        except:
            print "export api summary to file cause exception: %s" % file_path
        else:
            import pickle
            api_summaries_with_stacks, api_summaries_no_stacks = pickle.load(file)
            file.close()

            msg("%d - %d" % (len(api_summaries_with_stacks), len(api_summaries_no_stacks)))

            # print way borrowed from output.py

            if len(api_summaries_with_stacks) == 0:
                print "!" * 5 + " no api call with stacks " + "!" * 5
            else:
                print "!" * 5 + " api call with stacks count: %d " % len(api_summaries_with_stacks) + "!" * 5
                for record in api_summaries_with_stacks:
                    lines = record.lines()
                    for line in lines:
                        print "    %s" % line
                print ""

            if len(api_summaries_no_stacks) == 0:
                print "!" * 5 + " no api call with none stacks " + "!" * 5
            else:
                print "!" * 5 + " api call with none stacks count: %d " % len(api_summaries_no_stacks) + "!" * 5
                for record in api_summaries_no_stacks:
                    lines = record.lines()
                    for line in lines:
                        print "    %s" % line
                print ""
