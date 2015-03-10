#coding=utf-8

import numpy as np
import gzip
from sklearn.metrics import roc_auc_score

'''
    # 需要获得test set的true click => y
    # 和每次的预测prediction => p
    # 然后给auc_roc_score得出auc得分，看看趋势是不是和logloss一样
'''

click_path = '../result/test_click.gz'
gp_path = '../result/no_pred.gz'
bp_path = '../result/wt_pred.gz'

y_file = gzip.open(click_path)
gp_file = gzip.open(gp_path)
bp_file = gzip.open(bp_path)

y_file.readline()
gp_file.readline()
bp_file.readline()

y_list = []
gp_list = []
bp_list = []

for y_line in y_file.readlines():
    #每次读取出来，构建出y和p的array
    #id,click
    #id,pred
    y_temp = y_line.rstrip().split(',')[1]

    if y_temp == '0.000':
        y_list.append(0)
    else:
        y_list.append(1)

    gp_temp = gp_file.readline().rstrip().split(',')
    bp_temp = bp_file.readline().rstrip().split(',')
    gp_list.append(float(gp_temp[1]))
    bp_list.append(float(bp_temp[1]))

y_list = np.array(y_list)
gp_list = np.array(gp_list)
bp_list = np.array(bp_list)

print('get the array , calculate the auc score.')

gp_auc = roc_auc_score(y_list,gp_list)
bp_auc = roc_auc_score(y_list,bp_list)

print gp_auc,bp_auc
