#coding=utf-8

import sklearn.metrics
'''
key point is to change the csv_feat to vw_feat, so what about the namespace?! Is it meaning that the feat in one namespace is in one class or just means that it is one kind of feat like numerial or classlike...
after using like the later one, I think is to like one class of meaning but not kind of data. so rechange the feat in a new namespace construction.

feat: 1-ID:id, 2-click:0/1, 3-hour:2014120221, 4-C1:num_kind_cat, 5-banner_pos:num_kind_cat, 6-site_id:hash_val, 7-site_domain:hash_val, 8-site_category:hash_val, 9-app_id:hash_val, 10-app_domain:hash_val, 11-app_category:hash_val, 12-divice_id:hash_val, 13-divice_ip:hash_val, 14-divice_model:hash_val, 15-divice_type:num_kind_cat, 16-divice_conn_type:num_kind_cat, 17-C14-C21:num_kind_cat (C14,C17,C19,C20,C21)
'''
#first:mutual_info_score(label_true,label_pred,contingency=None), so get_single feat first.
feat_dict = {'ID':0,'click':1,'hour':2,'C1':3,'banner_pos':4,'site_id':5,'site_domain':6,'site_category':7,'app_id':8,'app_domain':9,'app_category':10,'divice_id':11,'divice_ip':12,'divice_model':13,'divice_type':14,'divice_conn_type':15,'C14':16,'C15':17,'C16':18,'C17':19,'C18':20,'C19':21,'C20':22,'C21':23}

#given the set and k, return the kth feat and the click.
def get_feat_click(tr_path,k):
    k_feat = []
    click = []
    first_line = True
    i_item = 1
    for line in open(tr_path,"rb"):
        if first_line:
            first_line = False
            continue
        feat_col = ""
        for idx,feat in enumerate(line.rstrip().split(',')):
            #given the name or the idx of the feat?
            if idx == 1:
                click.append(feat)
            if idx == k:
                k_feat.append(feat)
        i_item += 1
    return click,k_feat

#if the mi is small and small, it means that it is cuo! or is a category feat.
def get_MI(k_feat,click):
    mi = sklearn.metrics.mutual_info_score(click,k_feat)
    print mi

if __name__ == "__main__":
    #mi < 0.5 的 一般可以认为是特别挫的了
    #C1:cat. C14:0.035
    for i in feat_dict:
        click,k_feat = get_feat_click("../data/train.csv",feat_dict[i])
        print "this is about the %s feat."%(str(i))
        get_MI(click,k_feat)
