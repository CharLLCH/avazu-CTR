#coding=utf-8

'''
程序测试在29 30两天内的prediction和test的logloss
'''

from csv import DictReader
from math import log
import gzip

#gzip文件和正常文件除了open方式不同外，其他的应该是一样的

#拆分的时候就该把这个click的抽取出来，因为为了凑test将click消去了，这里已经没有clickkey了！
def get_test_click(path):
    outfile = gzip.open('../result/test_click.gz','wb')
    for idx,row in enumerate(DictReader(open(path))):
        ID = row['id']
        click = 0.
        if row['click'] == '1':
            click = 1.
        outfile.write('%s,%.3f\n' % (ID,click))


#logloss = -1/N \Sigma y_ij * log(p_ij)
def logloss(p,y):
    p = max(min(p,1. - 10e-15),10e-15)
    return -log(p) if y == 1. else -log(1. - p)

def get_logloss(pred_path,click_path):
    p_file = gzip.open(pred_path,'rb')
    y_file = gzip.open(click_path,'rb')
    
    #去掉第一行
    p_file.readline()
    y_file.readline()
    
    idx = 0
    loss = 0.
    for p_row in p_file.readlines():
        y = float(y_file.readline().strip().split(',')[1])
        p = float(p_row.strip().split(',')[1])
        #print '%.3f %.3f' %(y,p)
        idx += 1
        #p = 0. if p < 0.05 else p
        if p < 0.05:
            p = 0.
        #elif p > 0.5:
        #    p = 1.
        else:
            p = p
        loss += logloss(p,y)
        #print loss
    return loss / idx

if __name__ == "__main__":
    p_path = '../result/no_pred.gz'
    y_path = '../result/test_click.gz'
    loss = get_logloss(p_path,y_path)
    print 'totalloss',loss
    #get_test_click('../result/test_29_30.csv')
