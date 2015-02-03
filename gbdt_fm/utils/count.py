#!/usr/bin/env python3
#coding=utf-8

'''
    处理train.csv，具体需要根据不同的样本改了.

    原来 l1-lm个数字feat，和C1->C26个hash值feat，这里只统计了hash值的
    原来hash后的为cat，这里是不是像是cat的都扔进去？！
'''

import argparse, csv, sys, collections

from common import *

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('csv_path', type=str)
args = vars(parser.parse_args())

counts = collections.defaultdict(lambda : [0, 0, 0])

#算是预处理了，有Label，有C{0}..
for i, row in enumerate(csv.DictReader(open(args['csv_path'])), start=1):
    label = row['click']
    
    #统计各个fields的正负例数目，目测这里挑选出来的和后面的有联系
    #fields_dict = ['id','hour','C1','banner_pos','site_id','site_domain','site_category','app_id','app_domain','app_category','device_id','device_ip','device_model','device_type','device_conn_type','C14','C15','C16','C17','C18','C19','C20','C21']
    fields_dict = ['C1','banner_pos','site_id','site_domain','site_category','app_id','app_domain','app_category','device_id','device_ip','device_model','device_type','device_conn_type','C14','C15','C16','C17','C18','C19','C20','C21']

    for field in fields_dict:
        value = row[field]
        if label == '0':
            counts[field + ',' + value][0] += 1
        else:
            counts[field + ',' + value][1] += 1
        counts[field + ',' + value][2] += 1

    if i % 1000000 == 0:
        sys.stderr.write('{0}m\n'.format(int(i / 1000000)))

    '''
    for j in range(1, 27):
        field = 'C{0}'.format(j)
        value = row[field]
        if label == '0':
            counts[field+','+value][0] += 1
        else:
            counts[field+','+value][1] += 1
        counts[field+','+value][2] += 1
    if i % 1000000 == 0:
        sys.stderr.write('{0}m\n'.format(int(i/1000000)))
    '''

print('Field,Value,Neg,Pos,Total,Ratio')
for key, (neg, pos, total) in sorted(counts.items(), key=lambda x: x[1][2]):
    if total < 50:
        continue
    ratio = round(float(pos)/total, 5)
    print(key+','+str(neg)+','+str(pos)+','+str(total)+','+str(ratio))
