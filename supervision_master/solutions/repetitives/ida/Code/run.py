#!/usr/bin/python3
import os
import shutil
from multiprocessing import Pool


N = 8
M = 4
FIELD = 8

access_rights = 0o777
home_path = os.getcwd()

files_folder = 'files'
recov_folder = 'files_recovered'

file1 = 'file.txt'

dis = r'Dis'
rec = r'Rec'

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

    dispersal_file(tid,file1,N,M,FIELD)
    recovery_file(tid,file1,M,FIELD)


if __name__ == '__main__':
    
    # n_cores = len(os.sched_getaffinity(0)) # get the number of CPUs the current process can use
    # n_cores = (int(n_cores/2) if n_cores>1 else n_cores) # use half cores
    n_cores = 1 # ADDED, COMMENT THE TWO LINES BEFORE
    
    # for i in range(1,n_cores+1):
    #     print(f'BEGIN TEST with {i} workers')
    #     tuple_args = [(str(j)) for j in range(1,i+1)]
    #     with Pool(processes=i) as p:
    #         status = p.map( run_pipeline, tuple_args)
    #     print(f'END TEST with {i} workers')
    #     print()

    while True:
        print(f'BEGIN TEST with {n_cores} workers')
        tuple_args = [(str(j)) for j in range(1,n_cores+1)]
        with Pool(processes=n_cores) as p:
            status = p.map( run_pipeline, tuple_args)
        print(f'END TEST with {n_cores} workers')
        print()