#coding=utf-8

from datetime import datetime

def csv_to_vw(inpath,outpath,is_train=True):
    start = datetime.now()
    
    in_f = open(inpath,'r')
    out_f = open(outpath,'wb')

    counter = 0

    with in_f as infile:
        line_count = 0
        for line in infile:
            if line_count == 0:
                line_count == 1
                continue
            cat_feat = ''
            counter += 1
            line = line.split(",")

            if is_train:
                date_feat = line[2]
                new_date_feat = datetime(int("20"+date_feat[0:2]),int(date_feat[2:4]),int(date_feat[4:6]))
                day = new_date_feat.strftime("%A")
                hour = date_feat[6:8]
                cat_feat += " |hr %s" % hour
                cat_feat += " |dat %s" % day
                for feat in range(3,24):
                    if line[feat] != "":
                        cat_feat += "|c%s %s" % (str(feat),line[feat])
            else:
                date_feat = line[1]
                new_date_feat = datetime(int("20"+date_feat[0:2]),int(date_feat[2:4]),int(date_feat[4:6]))
                day = new_date_feat.strftime("%A")
                hour = date_feat[6:8]
                cat_feat += " |hr %s" % hour
                cat_feat += " |dat %s" % day
                for feat in range(2,23):
                    if line[feat] != "":
                        cat_feat += "|c%s %s" % (str(feat+1),line[feat])

            if is_train:
                if line[1] == "1":
                    click = 1
                else:
                    click = -1

                out_f.write( "%s '%s %s\n" % (click,line[0],cat_feat))
            else:
                out_f.write( "1 '%s %s\n" % (line[0],cat_feat))

            if counter % 1000000 == 0:
                print ("%s\t%s"%(counter,str(datetime.now()) - start)

if __name__ == "__main__":
    csv_to_vw('../data/train.csv','../result/newtrain.vw',is_train=True)
    csv_to_vw('../data/test.csv','../result/newtest.vw',is_train=False)
