#!/bin/python3
import os
from utils import JsonConfig, my_log_settings
import logging
from datetime import datetime
cwd = os.path.dirname(__file__)


def get_config_mtime():
    for dir in os.listdir(cwd):
        full_dir = os.path.join(cwd, dir)
        if not os.path.isdir(full_dir):
            continue
        for config in os.listdir(full_dir):
            if not config.endswith(".json"):
                continue
            full_json_file = os.path.join(full_dir, config)
            mtime = os.path.getmtime(full_json_file)
            j = JsonConfig(full_json_file, "rw")
            if "jsonver" not in j.data:
                j.update({"jsonver": "1.0.0"})
                j.dumpconfig()
            yield full_json_file, mtime


def gen_metadata(mtime_list: list):
    new_metadata = {}
    for line in mtime_list:
        r_path = os.path.relpath(line[0], cwd)
        name = os.path.basename(r_path)[0:-5]
        date=datetime.utcfromtimestamp(line[1])
        #date_str = date.strftime("%Y-%m-%d %H:%M:%S.%f")
        date_str=str(date)
        new_metadata.update({
            name: {
                "config_path": r_path,
                "date": date_str
            }
        })
    return new_metadata


if __name__ == "__main__":
    my_log_settings()
    j = JsonConfig(os.path.join(cwd, "metadata.json"), "rw")
    new_metadata = gen_metadata(get_config_mtime())
    if j.data == new_metadata:
        logging.info("metadata did not changed")
    else:
        j.dumpconfig(new_metadata)
