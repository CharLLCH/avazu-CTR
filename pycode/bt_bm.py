#coding=utf-8

from datetime import datetime
from csv import DictReader
from math import exp, log, sqrt
from pickle import dump, load
import gzip
from sys import argv, stdout, stderr
import random
import argparse

class ftrl_proximal(object):
    def __init__(self, alpha, beta, L1, L2, D, 
                 interaction=False, dropout = 1.0, sparse = False,
                 dayfeature = True,
                 device_counters = False):
        self.alpha = alpha
        self.beta = beta
        self.L1 = L1
        self.L2 = L2
        self.dayfeature = dayfeature
        self.device_counters = device_counters

        self.D = D
        self.interaction = interaction
        self.dropout = dropout        

        self.n = [0.] * D
        self.z = [0.] * D
        
        if sparse:
            self.w = {}
        else:
            self.w = [0.] * D  # use this for execution speed up

    def _indices(self, x):
        for i in x:
            yield i

        if self.interaction:
            D = self.D
            L = len(x)
            for i in xrange(1, L):  # skip bias term, so we start at 1
                for j in xrange(i+1, L):
                    # one-hot encode interactions with hash trick
                    yield abs(hash(str(x[i]) + '_' + str(x[j]))) % D

    def predict(self, x, dropped = None):
        dropout = self.dropout

        w = self.w

        wTx = 0.
        for j, i in enumerate(self._indices(x)):
            
            if dropped != None and dropped[j]:
                continue
           
            wTx += w[i]
        
        if dropped != None: wTx /= dropout 

        return 1. / (1. + exp(-max(min(wTx, 35.), -35.)))

    def update(self, x, y):
        alpha = self.alpha
        beta = self.beta
        L1 = self.L1
        L2 = self.L2

        n = self.n
        z = self.z
        w = self.w  # no need to change this, it won't gain anything
        dropout = self.dropout

        ind = [ i for i in self._indices(x)]
        
        if dropout == 1:
            dropped = None
        else:
            dropped = [random.random() > dropout for i in xrange(0,len(ind))]
        
        p = self.predict(x, dropped)

        g = p - y

        for j, i in enumerate(ind):

            if dropped != None and dropped[j]: continue

            sigma = (sqrt(n[i] + g * g) - sqrt(n[i])) / alpha
            z[i] += g - sigma * w[i]
            n[i] += g * g
            
            sign = -1. if z[i] < 0 else 1.  # get sign of z[i]

            if sign * z[i] <= L1:
                w[i] = 0.
            else:
                w[i] = (sign * L1 - z[i]) / ((beta + sqrt(n[i])) / alpha + L2)



def logloss(p, y):
    p = max(min(p, 1. - 10e-15), 10e-15)
    return -log(p) if y == 1. else -log(1. - p)


def data(f_train, D, dayfilter = None, dayfeature = True, counters = False):
    device_ip_counter = {}
    device_id_counter = {}

    for t, row in enumerate(DictReader(f_train)):
        ID = row['id']
        del row['id']

        y = 0.
        if 'click' in row:
            if row['click'] == '1':
                y = 1.
            del row['click']
 
        date = row['hour'][0:6]
        row['hour'] = row['hour'][6:]
        
        if dayfilter != None and not date in dayfilter:
            continue

        if dayfeature: 
            row['wd'] = str(int(date) % 7)
            row['wd_hour'] = "%s_%s" % (row['wd'], row['hour'])            

        if counters:
            d_ip = row['device_ip']
            d_id = row ["device_id"]
            try:
                device_ip_counter [d_ip] += 1
                device_id_counter [d_id] += 1
            except KeyError:
                device_ip_counter [d_ip] = 1
                device_id_counter [d_id] = 1                
            row["ipc"] = str(min(device_ip_counter[d_ip], 8))
            row["idc"] = str(min(device_id_counter[d_id], 8))

        x = [0]  # 0 is the index of the bias term
        for key in row:
            value = row[key]

            # one-hot encode everything with hash trick
            index = abs(hash(key + '_' + value)) % D
            x.append(index)

        yield t, ID, x, y

def myargs():
    
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description = 
""" 
Perform training and prediction based on FTRL Optimal algorithm, with dropout added.
\nUsage is via:
\n
\n\t* Training:
\n
\n\t\tpypy fastd.py train -t <train set> -o <output model> --<various parameters>
\n
\n\t* Predicting:
\n
\n\t\tpypy fastd.py predict --test <test set> -i <input model> -p <output predictions>
\n
""")
    parser.add_argument('action', type=str,
                        help='action to perform: train   / predict')
    parser.add_argument('-t', "--train", default = "/dev/stdin")
    parser.add_argument('--test', default = "/dev/stdin")
    parser.add_argument('-p', "--predictions", default = "/dev/stdout")
    parser.add_argument("-o", "--outmodel")
    parser.add_argument("-i", "--inmodel")
    parser.add_argument('--alpha', default = 0.015, type = float)
    parser.add_argument('--beta', default = 2, type = float)
    parser.add_argument('--L1', default = 0, type = float)
    parser.add_argument('--L2', default = 0, type = float)
    parser.add_argument('--dropout', default = 0.8, type = float)
    parser.add_argument('--bits', default = 23, type = int)
    parser.add_argument('--n_epochs', default = 1, type = int)
    parser.add_argument('--holdout', default = 100, type = int)
    parser.add_argument("--interactions", action = "store_true")
    parser.add_argument("--sparse", action = "store_true")
    parser.add_argument("-v", '--verbose', default = 3, type = int)
    parser.add_argument('--onlydays', default = None,  type = str,
                        help = "restrict to specific, comma-separated days")
    parser.add_argument("--nodayfeature", action = "store_true")
    parser.add_argument("--timefeature", action = "store_true",
                        help = "not yet implemented")
    parser.add_argument("--device_counters", action = "store_true",
                        help = "use device_ip and device_id counter as features")
  
    args = parser.parse_args()
    for v in vars(args).keys():
        stderr.write("%s => %s\n" % (v, str(vars(args)[v])))
        
    return args


def write_learner(learner, model_save, args):

   with gzip.open(model_save, "wb") as model_file:
           dump((args, learner),
                model_file)


def load_learner(model_save):
    
    with gzip.open(model_save, "rb") as model_file:
        (p, learner) = load(model_file)
    
    return learner
    

def train_learner(train, dayfilter, args):

    if args.verbose > 1:
        stderr.write("Learning from %s\n" % train)

    if train[-3:] == ".gz":
       f_train = gzip.open(train, "rb")
    else:
       f_train = open(train)
            
    start = datetime.now()
   
    D = 2**args.bits
    holdout = args.holdout
    dayfeaturep = not args.nodayfeature
    
        # initialize ourselves a learner
    learner = ftrl_proximal(args.alpha, args.beta, 
                           args.L1, args.L2, D, 
                           interaction = args.interactions,
                           dropout = args.dropout,
                           sparse = args.sparse,
                           dayfeature = dayfeaturep,
                           device_counters = args.device_counters)
            
        # start training
    for e in xrange(args.n_epochs):
       loss = 0.
       count = 0
       next_report = 10000
       c = 0
       
       if train != "/dev/stdin": f_train.seek(0,0)

       for t, ID, x, y in data(f_train, D, 
                               dayfilter = dayfilter,
                               dayfeature = dayfeaturep,
                               counters = args.device_counters):
           if t % holdout == 0:
                p = learner.predict(x)
                loss += logloss(p, y)
                count += 1
           else:
               learner.update(x, y)
            
           c += 1 
           if args.verbose > 2 and c >= next_report:
               stderr.write(' %s\tencountered: %d/%d\tcurrent logloss: %f\n' % (
                     datetime.now(), c, t, loss/count))
               next_report *= 2

       if count != 0:
           stderr.write('Epoch %d finished, %d/%d samples per pass, holdout logloss: %f, elapsed time: %s\n' % (
                    e, c, t, loss/count, str(datetime.now() - start)))
       else:
           stderr.write('Epoch %d finished, %d/%d samples per pass, suspicious holdout logloss: %f/%f, elapsed time: %s\n' % (
                  e, c, t, loss, count, str(datetime.now() - start)))

    f_train.close()

    return learner
    

def predict_learner(learner, test, predictions, dayfilter, args):
    
    if args.verbose > 1:
        stderr.write("Predicting to %s with model %s ...\n" % (predictions, str(learner)))        
    
    if test[-3:] == ".gz":
        f_test = gzip.open(test, "rb")
    else:
        f_test = open(test, "r")
        
    D = learner.D
    
    if not hasattr(learner, "device_counters"):
        learner.device_counters = False
     
    with gzip.open(predictions, 'wb') as outfile:
        outfile.write('id,click\n')
        for t, ID, x, y in data(f_test, D,
                                dayfilter = dayfilter,
                                dayfeature = learner.dayfeature,
                                counters = learner.device_counters):
            p = learner.predict(x)
            outfile.write('%s,%.3f\n' % (ID, p))
    
    f_test.close()


def main_fast_dropout():
    
    args = myargs()
    
    learner = None
   
    if args.onlydays == None:
        dayfilter = None
    else:
        dayfilter = args.onlydays.split(",")
        stderr.write("Considering only days %s...\n" % str(dayfilter))   
   
    if args.action in ["train", "train_predict"]:
        random.seed(1234)
        learner = train_learner(args.train, dayfilter, args)
        if args.outmodel != None:
            write_learner(learner, args.outmodel, args)
            
    if args.action in ["predict", "train_predict"]:
        random.seed(1234)
        if learner == None:
            learner = load_learner(args.inmodel)
        predict_learner(learner, args.test, args.predictions, dayfilter, args)
        
    return learner        
        
if __name__ == "__main__":
    main_fast_dropout()

