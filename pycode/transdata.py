#coding=utf-8

from csv import DictReader

def get_raw_data(inpath,outpath):
    t_file = open(inpath)
    nt_file = open(outpath,'wb')

    #click做y，剩下的除了id做x，需要把key加上，time再加工下？
    for idx,row in enumerate(DictReader(t_file)):
        time_date = 'time-' + str(row['hour'][4:6])
        del row['hour']
        
        y = 0
        if 'click' in row:
            if row['click'] == '1':
                y = 1
            else:
                y = -1
            del row['click']

        nt_file.write('%d,%s'%(y,time_date))

        for keys in row:
            nt_file.write(',%s'%(keys+'-'+str(row[keys])))
        nt_file.write('\n')

    nt_file.close()

if __name__ == "__main__":
    tr_path = '../result/train_21_28.csv'
    te_path = '../result/test_29_30.csv'
    otr_path = '../../libfm-1.42.src/scripts/traint.dat'
    ote_path = '../../libfm-1.42.src/scripts/test.dat'
    #get_raw_data(te_path,ote_path)
    get_raw_data(tr_path,otr_path)
