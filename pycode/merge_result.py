#coding=utf-8

import gzip

def merge_result(in_1,in_2,out_path,methods):
    infile_x = gzip.open(in_1,'rb')
    infile_y = gzip.open(in_2,'rb')

    outfile = gzip.open(out_path,'wb')

    line = infile_y.readline()
    infile_x.readline()

    outfile.write(line)

    holdout = 0.5
    hold_dw = 0.05
    hold_up = 0.85

    idx = 1
    for x_line in infile_x.readlines():
        y = float(infile_y.readline().rstrip().split(',')[1])
        x_list = x_line.strip().split(',')
        x = float(x_list[1])


        if (methods == True):
            if x < hold_dw and y < hold_dw:
                if x < y:
                    z = x
                else:
                    z = y
            elif x > hold_up and y > hold_up:
                if x > y:
                    z = x
                else:
                    z = y
            else:
                z = (x+y) / 2.
        else:
            if x < hold_dw and y < hold_dw:
                if x < y:
                    z = y
                else:
                    z = x
            elif x > hold_up and y > hold_up:
                if x < y:
                    z = x
                else:
                    z = y
            else:
                z = (x + y) / 2.

        outfile.write('%s,%f\n'%(x_list[0],z))
        idx += 1
        if idx % 10000 == 0:
            print(" %d 0000"%(idx/10000))

    outfile.close()
    infile_y.close()
    infile_x.close()


if __name__ == "__main__":
    in_x = '../data/L7N3D8sub.gz'
    in_y = '../data/L157N4D8sub.gz'
    out_path = '../data/mergesub-1.gz'

    merge_result(in_x,in_y,out_path,False)
