#coding=utf-8

from csv import DictReader

def get_count(inpath):
    
    infile = open(inpath)

    pos_dict = {}

    ratio_dict = {}
    
    for idx,row in enumerate(DictReader(infile)):

        if row['Field'] in pos_dict:
            pos_dict[row['Field']] += 1
            ratio_dict[row['Field']][0] += float(row['Ratio'])
            ratio_dict[row['Field']][1] += int(row['Total'])
        else:
            pos_dict[row['Field']] = 1
            ratio_dict[row['Field']] = list()
            ratio_dict[row['Field']].append(float(row['Ratio']))
            ratio_dict[row['Field']].append(int(row['Total']))

    for idx in pos_dict:
        print "ValueCount : %d \t TimesCount : %d \t RatioAvg : %f \t feature:%s"%(pos_dict[idx],ratio_dict[idx][1],ratio_dict[idx][0]*1./pos_dict[idx],idx)


if __name__ == "__main__":

    inpath = 'positive_count.txt'

    get_count(inpath)
