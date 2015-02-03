#!/usr/bin/env python3

import subprocess, sys, os, time

NR_THREAD = 2

start = time.time()

cmd = 'converters/parallelizer-a.py -s {nr_thread} converters/pre-a.py tr.csv tr.gbdt.dense tr.gbdt.sparse'.format(nr_thread=NR_THREAD)
subprocess.call(cmd, shell=True) 

cmd = 'converters/parallelizer-a.py -s {nr_thread} converters/pre-a.py te.csv te.gbdt.dense te.gbdt.sparse'.format(nr_thread=NR_THREAD)
subprocess.call(cmd, shell=True) 

print('preprocessing over and time used = {0:.0f}'.format(time.time()-start))

cmd = './gbdt -t 30 -s {nr_thread} te.gbdt.dense te.gbdt.sparse tr.gbdt.dense tr.gbdt.sparse te.gbdt.out tr.gbdt.out'.format(nr_thread=NR_THREAD) 
subprocess.call(cmd, shell=True)

#cmd = 'rm -f te.gbdt.dense te.gbdt.sparse tr.gbdt.dense tr.gbdt.sparse'
#subprocess.call(cmd, shell=True)

print('GBDT over and time used = {0:.0f}'.format(time.time()-start))

cmd = 'converters/parallelizer-b.py -s {nr_thread} converters/pre-b.py tr.csv tr.gbdt.out tr.fm'.format(nr_thread=NR_THREAD)
subprocess.call(cmd, shell=True) 

cmd = 'converters/parallelizer-b.py -s {nr_thread} converters/pre-b.py te.csv te.gbdt.out te.fm'.format(nr_thread=NR_THREAD)
subprocess.call(cmd, shell=True) 

#cmd = 'rm -f te.gbdt.out tr.gbdt.out'
#subprocess.call(cmd, shell=True) 

print('second processing over and time used = {0:.0f}'.format(time.time()-start))

cmd = './fm -k 4 -t 11 -s {nr_thread} te.fm tr.fm'.format(nr_thread=NR_THREAD) 
subprocess.call(cmd, shell=True)

cmd = './utils/calibrate.py te.fm.out te.fm.out.cal'.format(nr_thread=NR_THREAD) 
subprocess.call(cmd, shell=True)

cmd = './utils/make_submission.py te.fm.out.cal submission.csv'.format(nr_thread=NR_THREAD) 
subprocess.call(cmd, shell=True)

print('total time used = {0:.0f}'.format(time.time()-start))
