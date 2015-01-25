#coding=utf-8

import gzip

def adjust_result(in_path,out_path):
	"试着将过小或者过大的调整一下"

	infile = gzip.open(in_path,'rb')
	outfile = gzip.open(out_path,'wb')

	infile.readline()
	outfile.write('id,click\n')

	for line in infile.readlines():

		items = line.strip().split(',')

		y = float(items[1])

		p = 0.
		
		if y < 0.05:
			p = 0.

		else:
			p = y

		outfile.write('%s,%.3f\n'%(items[0],p))

	infile.close()
	outfile.close()

if __name__ == "__main__":
	in_path = '../result/L5N4D7sub.gz'
	out_path = '../result/L5N4D7subadj.gz'
	adjust_result(in_path,out_path)
