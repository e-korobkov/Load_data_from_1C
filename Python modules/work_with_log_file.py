import os
import get_catalogs_ways as gt
import datetime


def write_to_log(parent_path, line) -> None:
    check_log_file(parent_path)
    d = gt.get_catalogs_way(parent_path)
    way = f"{d.get('log_file')}\\log_file.txt"
    f = open(way, 'a')
    with f:
        line = f"{datetime.datetime.now()} *** {line}"
        f.write(line + '\n')


def check_log_file(parent_path):
    d = gt.get_catalogs_way(parent_path)
    check_file = os.path.exists(f"{d.get('log_file')}\\log_file.txt")
    if check_file is False:
        way = f'{d.get("log_file")}\\log_file.txt'
        f = open(way, 'w')
        f.close()
