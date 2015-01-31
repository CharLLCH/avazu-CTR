#coding=utf-8

'''
测试fm结果
'''

from math import log
import gzip

def logloss(p,y):
    "获得单个预测和点击的logloss值"

    return -log(p) if y == 1. else -log(1. - p)

def get_logloss(pred_path,click_path):
    "获得所有预测和实际点击的logloss值"

    pred_file = open(pred_path,'rb')
    click_file = gzip.open(click_path,'rb')
    
    click_file.readline()

    idx = 0
    loss = 0.

    for pred in pred_file.readlines():
        
        y = float(click_file.readline().strip().split(',')[1])
        p = float(pred.strip())

        idx += 1

        loss += logloss(p,y)

    return loss / idx

if __name__ == '__main__':
    pred_path = '../result/prediction'
    click_path = '../result/test_click.gz'
    loss = get_logloss(pred_path,click_path)
    print "total loss : ",loss
