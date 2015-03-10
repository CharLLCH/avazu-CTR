#coding=utf-8

from csv import DictReader
from csv import DictWriter
import pickle
import gzip

tr_path = '../data/train.csv'
te_path = '../data/test.csv'

#获得FIELDS，和日期,date：21-30，测试31！
def get_fields_days(path):

    fields_geted = False

    days_dict = {}

    for idx,row in enumerate(DictReader(open(path))):

        time_feat = row['hour']
        time_date = time_feat[4:6]
        
        if fields_geted == False:
            fields = row.keys()
            field_file = open('../result/fields.pkl','wb')
            pickle.dump(fields,field_file,True)
            fields_geted = True

        if time_date not in days_dict:
            days_dict[time_date] = 1
    days_file = open('../result/dates.pkl','wb')
    pickle.dump(days_dict,days_file,True)

#根据日期，将训练集分开
def split_train(path):
    infile = open('../result/fields.pkl','rb')
    TR_FIELDS = pickle.load(infile)
    #print TR_FIELDS
    TE_FIELDS = [item for item in TR_FIELDS if item !='click']
    #print TE_FIELDS
    
    new_tr_file = open('../result/train_21_28.csv','wb')
    new_te_file = open('../result/test_29_30.csv','wb')
    click_file = gzip.open('../result/test_click.gz','wb')
    
    tr_writer = DictWriter(new_tr_file,fieldnames=TR_FIELDS)
    te_writer = DictWriter(new_te_file,fieldnames=TE_FIELDS)

    #第一行得自己写！
    tr_writer.writerow(dict(zip(TR_FIELDS,TR_FIELDS)))
    te_writer.writerow(dict(zip(TE_FIELDS,TE_FIELDS)))
    click_file.write('id,click\n')

    for idx,row in enumerate(DictReader(open(path))):
        
        time_date = int(row['hour'][4:6])

        if time_date < 29:
            tr_writer.writerow(row)
        else:

            y = 0.
            if row['click'] == '1':
                y = 1.
            click_file.write('%s,%.3f\n' % (row['id'],y))
            del row['click']
            te_writer.writerow(row)
    
    new_te_file.close()
    new_tr_file.close()
    click_file.close()


if __name__ == "__main__":
    #get_fields_days(tr_path)
    split_train(tr_path)
