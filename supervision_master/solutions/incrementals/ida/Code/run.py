#!/usr/bin/python3
# Execution command: python3 run.py -c 10MB.txt-100MB.txt-1000MB.txt
"""
c = size of files in MB splited by mid slash
files with the specified size must be created in files/ folder
"""
import os
import argparse
import shutil
import time
import numpy as np
from multiprocessing import Pool


N = 8
M = 4
FIELD = 8

dis = r'Dis'
rec = r'Rec'

files_folder = 'files'
recov_folder = 'files_recovered'

access_rights = 0o777
home_path = os.getcwd()


def create_subfolders(path,access_rights):
    cr = None
    try:
        if not os.path.exists(path):
            os.makedirs(path, access_rights)
            cr = 1
    except OSError:
        print(f'Creation of the directory failed')
        print(path)
    return cr

def dispersal_file(th_id, file, n, m, field):
    # print('dispersal_file')

    sentence = './Dis '+str(n)+' '+str(m)+' '+str(field)+' ../../'+files_folder+'/'+file
    os.system(sentence)

    return 'disperse file'

def recovery_file(th_id, file, m, field):
    # print('recovery_file')

    dispersed_files = [x for x in os.listdir('./') if len(x) == 2]
    sentence = './Rec ' + file + ' ' + str(field)

    for i in range(0, m):
        sentence = sentence + ' ./' + dispersed_files[i]
    os.system(sentence)

    for k in dispersed_files:
        remove = 'rm ./' + k
        # print(remove)
        os.system(remove)

    return 'recovery file'

def run_pipeline(tuple):
    tid = tuple[0]
    cfile = tuple[1]

    t_path = os.sep.join([home_path, recov_folder, tid])
    create_subfolders(t_path,access_rights)

    t_p_dis = os.sep.join([t_path, dis])
    shutil.copyfile(dis, t_p_dis)
    os.system('chmod +x '+t_p_dis)

    t_p_rec = os.sep.join([t_path, rec])
    shutil.copyfile(rec, t_p_rec)
    os.system('chmod +x '+t_p_rec)

    os.chdir( t_path )
    print(os.getcwd())

    dispersal_file(tid,cfile,N,M,FIELD)
    recovery_file(tid,cfile,M,FIELD)

def parse_arguments():
    """Define and parse arguments passed by flags to the program

    Returns:
        ArgumentParser: object with all arguments
    """
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-c','--configs', help='Desc', required=True)
    return parser.parse_args()

if __name__ == '__main__':
    time.sleep(1)
    args = parse_arguments()
    
    # get the number of CPUs the current process can use
    cores = len(os.sched_getaffinity(0))
    # use half cores
    # cores = (int(cores/2) if cores>1 else cores)
    configs = args.configs.split('-')
    num = len(configs)
    n_cores = np.linspace(start=1, stop=cores, num=num)

    for i,c in enumerate(configs):
        i = i+1
        print(f'BEGIN {c} with {i} workers')
        tuple_args = [(str(j),c) for j in range(1,i+1)]
        with Pool(processes=i) as p:
            status = p.map( run_pipeline, tuple_args)
        print(f'END {c} with {i} workers')
        print()
    time.sleep(1)
