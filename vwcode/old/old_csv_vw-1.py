#coding=utf-8

from csv import DictReader
import hashlib
from datetime import datetime

def change_to_vw(in_path,out_path,if_train=True):
    start_time = datetime.now()
    print "start at time: %s "%start_time
    with open(out_path,"wb") as outfile:
        '''
        for idx,row in enumerate(DictReader(open(in_path))):
            num_feat = ""
            cat_feat = ""
            for n_feat,v_feat in row.items():
                if n_feat not in ["id","click"]:
                    if "C" not in n_feat:
                        #cat type feat
                        if len(str(v_feat)) > 0:
                            cat_feat += " %s"%v_feat
                    else:
                        if len(str(v_feat)) > 0:
                            num_feat += " %s"%v_feat
            if if_train:
                if row["click"] == "1":
                    label = 1
                else:
                    label = 0
                outfile.write("%s '%s |i%s |c%s\n"%(label,row["id"],num_feat,cat_feat))
            else:
                outfile.write("1 '%s |i%s |c%s\n"%(row["id"],num_feat,cat_feat))
        '''
        i = 1
        #D = 2**24
        first = True
        for line in open(in_path,"rb"):
            if first:
                first = False
                continue
            num_feat = ""
            cat_feat = ""
            for idx,row in enumerate(line.rstrip().split(',')):
                if idx == 0:
                    ids = row
                elif if_train and idx == 1:
                    if row == "1":
                        click = 1
                    else:
                        click = -1
                elif not if_train and idx == 1:
                    #hour only feat treat as num
                    num_feat += " hour:%s"%row
                elif if_train and idx == 2:
                    num_feat += " hour:%s"%row
                elif idx < 5:
                    #cat_feat += " %s"%str(int(hashlib.md5(row.encode('utf-8')).hexdigest(),16)%D)
                    cat_feat += " %s"%row
                elif idx < 14:
                    cat_feat += " %s"%row
                else:
                    #cat_feat += " %s"%str(int(hashlib.md5(row.encode('utf-8')).hexdigest(),16)%D)
                    cat_feat += " %s"%row
            if if_train:
                outfile.write("%s '%s |i%s |c%s\n"%(click,ids,num_feat,cat_feat))
            else:
                outfile.write("1 '%s |i%s |c%s\n"%(ids,num_feat,cat_feat))
            if i % 100000 == 0:
                print "handler %s items..."%(str(i))
                print "used time %s"%(str(datetime.now()-start_time))
            i += 1
    print "total time is : %s"%(str(datetime.now() - start_time))

if __name__ == "__main__":
    change_to_vw("../data/train.csv","../data/train_vw.vw",True)
    change_to_vw("../data/test.csv","../data/test_vw.vw",False)
