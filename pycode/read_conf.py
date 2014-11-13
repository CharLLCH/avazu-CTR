#coding=utf-8
#read the conf_path of the data
#use the dict format, result['path'] = path

import sys

def config(fn):
    with open(fn,"rb") as infile:
        result = {}
        for line in infile.readlines():
            if len(line) < 4 or line[0] == "#":
                pass
            else:
                sp = line.split()
                result[sp[0]] = sp[2]
    infile.close()
    return result
