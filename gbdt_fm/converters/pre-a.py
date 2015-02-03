#!/usr/bin/env python3
#coding=utf-8

'''
    转换出需要的dense和sparse矩阵，同时根据target_cat_feat筛选..
    分别创建dense和sparse！
'''

import argparse, csv, sys

from common import *

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('csv_path', type=str)
parser.add_argument('dense_path', type=str)
parser.add_argument('sparse_path', type=str)
args = vars(parser.parse_args())

#可以用common里面的get_frequent_feats来当target么！？

target_cat_feats = ['C16-50','C15-320','device_type-1','C1-1005','app_category-07d7df22','site_category-50e219e0','C18-0','C21-23','C17-1722','C20-100084','C19-39']

with open(args['dense_path'],'w') as f_d, open(args['sparse_path'],'w') as f_s:
    for row in csv.DictReader(open(args['csv_path'])):
        
        feats = []
        val = row['hour']
        if val == '':
            val = -10
        feats.append('{0}'.format(val))
        f_d.write(row['click'] + ' ' + ' '.join(feats) + '\n')

        cat_feats = set()
        fields_dict = ['C1','banner_pos','site_id','site_domain','site_category','app_id','app_domain','app_category','device_id','device_ip','device_model','device_type','device_conn_type','C14','C15','C16','C17','C18','C19','C20','C21']
        for field in fields_dict:
            key = field + '-' + row[field]
            cat_feats.add(key)

        feats = []
        for idx,feat in enumerate(target_cat_feats,start = 1):
            if feat in cat_feats:
                feats.append(str(idx))
        f_s.write(row['click'] + ' ' + ' '.join(feats) + '\n')

'''
    #首先，target_cat_feat不知道选谁还..
    #然后，具体的feat fields也不同
    #最后，一个dense都没有可不可以啊..

target_cat_feats = ['C9-a73ee510', 'C22-', 'C17-e5ba7672', 'C26-', 'C23-32c7478e', 'C6-7e0ccccf', 'C14-b28479f6', 'C19-21ddcdc9', 'C14-07d13a8f', 'C10-3b08e48b', 'C6-fbad5c96', 'C23-3a171ecb', 'C20-b1252a9d', 'C20-5840adea', 'C6-fe6b92e5', 'C20-a458ea53', 'C14-1adce6ef', 'C25-001f3601', 'C22-ad3062eb', 'C17-07c540c4', 'C6-', 'C23-423fab69', 'C17-d4bb7bd8', 'C2-38a947a1', 'C25-e8b83407', 'C9-7cc72ec2']

with open(args['dense_path'], 'w') as f_d, open(args['sparse_path'], 'w') as f_s:
    for row in csv.DictReader(open(args['csv_path'])):
        feats = []
        for j in range(1, 14):
            val = row['I{0}'.format(j)]
            if val == '':
                val = -10 
            feats.append('{0}'.format(val))
        f_d.write(row['Label'] + ' ' + ' '.join(feats) + '\n')
        
        cat_feats = set()
        for j in range(1, 27):
            field = 'C{0}'.format(j)
            key = field + '-' + row[field]
            cat_feats.add(key)

        feats = []
        for j, feat in enumerate(target_cat_feats, start=1):
            if feat in cat_feats:
                feats.append(str(j))
        f_s.write(row['Label'] + ' ' + ' '.join(feats) + '\n')
'''
