#coding=utf-8

import math

def zymoid(x):
    return 1 / ( 1 + math.exp(-x) )

with open('../result/vw_submit.csv','wb') as outfile:
    outfile.write("id,click\n")
    for line in open('../result/pred_vw.txt'):
        row = line.strip().split(" ")
        try:
            outfile.write("%s,%f\n"%(row[1],zymoid(float(row[0]))))
        except:
            pass
