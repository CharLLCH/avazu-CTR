#coding=utf-8
from __future__ import division
import numpy as np
import pandas as pd
import cPickle
from read_conf import config
from sklearn import preprocessing

t_path = config("../conf/dp.conf")
tr_path = t_path["train_data_path"]
te_path = t_path["test_data_path"]

D = 2 ** 20

def get_data(path,tr=False):
    for t,line in enumerate(open(path)):
        if t == 0:
            x = [0]*27
            continue
        for m,feat in enumerate(line.rstrip().split(',')):
            if m == 0:
                ID = int(feat)
            elif tr and m == 1:
                y = [float(feat)]
            else:
                x[m] = abs(hash(str(m) + '_' + feat)) % D
        yield (ID,x,y) if tr else (ID,x)

def get_feat(path,tr,num_feat):
    for t,line in enumerate(open(path)):
        if t == 0:
            feat_list = []
            id_list = []
            y_list = []
            id_tmp = 0
            y_tmp = 0.0
            continue
        for m,feat in enumerate(line.rstrip().split(',')):
            if m == 0:
                id_tmp = int(feat)
            elif tr and m == 1:
                y_tmp = [float(feat)]
            elif m == num_feat:
                id_list.append(id_tmp)   
                y_list.append(y_tmp)
                feat_list.append(abs(hash(str(m)+'_'+feat))%D)
                print id_tmp,feat_list[-1],feat
    return id_list,y_list,feat_list
        
if __name__ == "__main__":
    id,y,feat = get_feat(tr_path,True,7)
    enc = preprocessing.OneHotEncoder()
    enc.fit(feat)
    enc.transform(feat[-1])
