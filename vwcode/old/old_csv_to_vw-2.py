#coding=utf-8

from datetime import datetime
import hashlib

def csv_to_vw(inpath,outpath,if_train=True):
    s_time = datetime.now()
    with open(outpath,'wb') as outfile:
        D = 2 ** 32
        first_line = True
        lines = 0
        for line in open(inpath,'rb'):
            if first_line:
                first_line = False
                continue
            cat_feat = ''
            date_feat = ''
            p_id = ''
            click = 0
            start_date = 14102100
            for idx,feat in enumerate(line.rstrip().split(',')):
                if idx == 0:
                    p_id = feat
                elif if_train and idx == 1:
                    if feat == "1":
                        click = 1
                    else:
                        click = -1
                elif not if_train and idx == 1:
                    date_feat = " hour:%s"%str(int(feat)-start_date)
                elif if_train and idx == 2:
                    date_feat = " hour:%s"%str(int(feat)-start_date)
                else:
                    #MD5-digest()-16bits,hexdigest()-32bits,Sha1 digest()-20bits,hexdigest()-40bits.
                    cat_feat += " %s:%s"%(str(idx),str(int(hashlib.md5(feat.encode('utf-8')).hexdigest(),16)%D))
            if if_train:
                outfile.write("%s '%s |%s |%s\n"%(click,p_id,date_feat,cat_feat))
            else:
                outfile.write("1 '%s |%s |%s\n"%(p_id,date_feat,cat_feat))
            if lines % 500000 == 0:
                print lines
                print date_feat,cat_feat
            lines += 1
        outfile.close()

if __name__ == "__main__":
    csv_to_vw('../data/train.csv','../result/train_vw.vw',True)
    csv_to_vw('../data/test.csv','../result/test_vw.vw',False)
