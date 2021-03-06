#!/usr/bin/env python3
#coding=utf-8

'''
    对test.csv加入了click列..全'0'，将code中所有fields全部替换成当前的
'''

import argparse, csv, hashlib

parser = argparse.ArgumentParser(description='process some integers')
parser.add_argument('csv_path', type=str, nargs=1, help='set path to the csv file')
parser.add_argument('out_path', type=str, nargs=1, help='set path to the svm file')
args = parser.parse_args()

CSV_PATH, OUT_PATH = args.csv_path[0], args.out_path[0]

f = csv.writer(open(OUT_PATH, 'w'))
for i, row in enumerate(csv.reader(open(CSV_PATH))):
    if i == 0:
        row.insert(1, 'click')
    else:
        row.insert(1, '0')
    f.writerow(row)
