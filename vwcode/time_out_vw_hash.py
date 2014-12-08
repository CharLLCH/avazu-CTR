#coding=utf-8

import hashlib

def csv_to_vw(inpath,outpath,is_train=True):
    counter = 0
    #D = 10 ** 6

    with open(outpath,'wb') as outfile:
        first_line = True
        for lines in open(inpath,'rb'):
            if first_line:
                first_line = False
                continue
            cat_feat = ''
            line = lines.rstrip().split(',')
            if is_train:
                for feat in range(3,24):
                    if line[feat] != "":
                        #cat_feat += "|c%s %s"%(str(feat),str(int(hashlib.md5(line[feat].encode('utf-8')).hexdigest(),16)%D+1))
                        tmp_str = "C"+str(feat)+'-'+line[feat]
                        cat_feat += "|c%s %s"%(str(feat),tmp_str)
            else:
                for feat in range(2,23):
                    if line[feat] != "":
                        #cat_feat += "|c%s %s"%(str(feat+1),str(int(hashlib.md5(line[feat].encode('utf-8')).hexdigest(),16)%D+1))
                        tmp_str = "C"+str(feat+1)+'-'+line[feat]
                        cat_feat += "|c%s %s"%(str(feat+1),tmp_str)

            if is_train:
                if line[1] == "1":
                    click = 1
                else:
                    click = -1
                outfile.write("%s '%s %s\n"%(click,line[0],cat_feat))
            else:
                outfile.write("1 '%s %s\n"%(line[0],cat_feat))

            if counter % 1000000 == 0:
                print counter
            counter += 1

if __name__ == "__main__":
    csv_to_vw('../data/train.csv','../result/tr_t_out_vw_hash.vw',True)
    csv_to_vw('../data/test.csv','../result/te_t_out_vw_hash.vw',False)
