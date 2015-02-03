#coding=utf-8

import gzip

def fm_to_gzip(p_path,m_path,s_path):
    '''prediction to submit.'''
    
    p_file = open(p_path,'rb')
    m_file = gzip.open(m_path,'rb')
    s_file = gzip.open(s_path,'wb')

    m_file.readline()

    s_file.write('id,click\n')
    
    for line in p_file.readlines():
        
        prediction = float(line.strip())

        p_id = m_file.readline().strip().split(',')[0]

        s_file.write('%s,%f\n'%(p_id,prediction))

    p_file.close()
    m_file.close()
    s_file.close()


if __name__ == "__main__":
    
    p_path = '../libfm-r/libfm'
    m_path = '../libfm-r/lr.gz'
    s_path = '../libfm-r/libfm.gz'

    fm_to_gzip(p_path,m_path,s_path)
