#coding=utf-8
from datetime import datetime
from math import log, exp, sqrt
from read_conf import config

# parameters #################################################################
#train_data_path  # path to training file
#train/test_header_path # path to label file of training data
#test_data_path # path to testing file

t_path = config("../conf/dp.conf")
train_data_path = t_path["train_data_path"]
test_data_path = t_path["test_data_path"]
#train_header_path = t_path["train_header_path"]
#test_header_path = t_path["test_header_path"]

D = 2 ** 20  # number of weights use for each model, we have 32 of them
#用hash值做数组index来操作的
alpha = .1   # learning rate for sgd optimization

#粗暴的简单预处理，具体的feat可以具体考虑，而不是单一的直接hash掉
#traindata-optional,Set to True to handle trainset,ignore it thus testset
def data(path, traindata=False):
    for t, line in enumerate(open(path)):
        if t == 0:
            x = [0] * 27
            continue
        #single line of id,y,feats..
        for m, feat in enumerate(line.rstrip().split(',')):
            if m == 0:
                ID = int(feat)
            elif traindata and m == 1:
                y = [float(feat)]
            else:
                x[m] = abs(hash(str(m) + '_' + feat)) % D

        yield (ID, x, y) if traindata else (ID, x)

#误差，用来梯度下降更新weight
def logloss(p, y):
    p = max(min(p, 1. - 10e-15), 10e-15)
    return -log(p) if y == 1. else -log(1. - p)

#预测，sigmoid！
def predict(x, w):
    wTx = 0.
    for i in x:  # do wTx
        wTx += w[i] * 1.  # w[i] * x[i], but if i in x we got x[i] = 1.
    return 1. / (1. + exp(-max(min(wTx, 20.), -20.)))  # bounded sigmoid

#根据预测的值和trainset中值进行比较，更新权值
def update(alpha, w, n, x, p, y):
    for i in x:
        # alpha / sqrt(n) is the adaptive learning rate
        # (p - y) * x[i] is the current gradient
        # note that in our case, if i in x then x[i] = 1.
        n[i] += abs(p - y)
        w[i] -= (p - y) * 1. * alpha / sqrt(n[i])

start = datetime.now()
#K : the number of the categories of y! Here just click or not, 0 - 1
K = [0]
w = [[0.] * D]
n = [[0.] * D]
loss = 0.
tt = 1
#wait wait, w also the dicttype!? if I meet the same featval I use its weight!?
#ID,x is the list of feats,y is the pred!
for ID, x, y in data(train_data_path, traindata = True):
    # get predictions and train on all labels
    for k in K:
        p = predict(x, w[k])
        update(alpha, w[k], n[k], x, p, y[k])
        loss += logloss(p, y[k])  # for progressive validation
    if tt % 100000 == 0:
        print('%s\tencountered: %d\tcurrent logloss: %f' % (
                datetime.now(), tt, (loss * 1./tt)))
    tt += 1

with open('../result/sub.csv', 'wb') as outfile:
    outfile.write('id,click\n')
    for ID, x in data(test_data_path):
        for k in K:
            p = predict(x, w[k])
            outfile.write('%s,%s\n' % (ID, str(p)))

print('Done, elapsed time: %s' % str(datetime.now() - start))
