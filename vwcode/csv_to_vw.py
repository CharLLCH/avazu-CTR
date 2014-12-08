#coding=utf-8

from datetime import datetime
import hashlib

def csv_to_vw(inpath,outpath,is_train=True):
    start = datetime.now()
    
    #infile = open(inpath,'rb')
    #out_f = open(outpath,'wb')

    counter = 0
    D = 10 ** 6

    with open(outpath,'wb') as out_file:
        line_count = 0
        for lines in open(inpath,'rb'):
            if line_count == 0:
                line_count = 1
                continue
            cat_feat = ''
            counter += 1
            line = lines.rstrip().split(',')
            if is_train:
                date_feat = line[2]
                new_date_feat = datetime(int("20"+date_feat[0:2]),int(date_feat[2:4]),int(date_feat[4:6]))
                day = new_date_feat.strftime("%A")
                hour = date_feat[6:8]
                cat_feat += " |hr %s" % hour
                cat_feat += " |dat %s" % day
                for feat in range(3,24):
                    if line[feat] != "":
                        #cat_feat += "|c%s %s" % (str(feat),line[feat])
                        cat_feat += "|c%s %s" % (str(feat),str(int(hashlib.md5(line[feat].encode('utf-8')).hexdigest(),16)%D+1))
            else:
                date_feat = line[1]
                new_date_feat = datetime(int("20"+date_feat[0:2]),int(date_feat[2:4]),int(date_feat[4:6]))
                day = new_date_feat.strftime("%A")
                hour = date_feat[6:8]
                cat_feat += " |hr %s" % hour
                cat_feat += " |dat %s" % day
                for feat in range(2,23):
                    if line[feat] != "":
                        #cat_feat += "|c%s %s" % (str(feat+1),line[feat])
                        cat_feat += "|c%s %s" % (str(feat+1),str(int(hashlib.md5(line[feat].encode('utf-8')).hexdigest(),16)%D+1))

            if is_train:
                if line[1] == "1":
                    click = 1
                else:
                    click = -1
                out_file.write( "%s '%s %s\n" % (click,line[0],cat_feat))
            else:
                out_file.write( "1 '%s %s\n" % (line[0],cat_feat))

            if counter % 1000000 == 0:
                print ("%s\t%s"%(counter,str(datetime.now() - start)))
                print cat_feat

if __name__ == "__main__":
    csv_to_vw('../data/train.csv','../result/newtrain.vw',True)
    csv_to_vw('../data/test.csv','../result/newtest.vw',False)
