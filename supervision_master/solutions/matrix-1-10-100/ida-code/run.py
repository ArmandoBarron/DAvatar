#!/usr/bin/python3
import os
import shutil
import argparse
import time


"""
INPUT
"""
N = 8
M = 4
FIELD = 8
input_folder = 'input'
file1 = 'file.txt'

"""
OUTPUT
"""
output_folder = 'output'

"""
FUNCTIONS
"""
dis = r'Dis'
rec = r'Rec'


access_rights = 0o777
home_path = os.getcwd()
ID = os.environ['SOL_ID']+'-'+os.environ['W_ID']

def create_subfolders(path,access_rights):
    """Create folders.

    Create folders and subfolders in path with specific access rights.

    Args:
        path (str): Path to create folders
        access_rights (int): Access rights to apply to every folder created

    Returns:
        bool: True if created False if not

    """
    cr = False
    try:
        if not os.path.exists(path):
            os.makedirs(path, access_rights)
            cr = True
        else:
            cr = True
    except OSError:
        print(f'Creation of the directory failed')
        print(path)
    return cr


def dispersal_file(wkr_id, file, n, m, field):
    """Disperse file.

    Disperse file to n chunks with the posibility to recover with m of those chunks.

    Args:
        wkr_id (str): Id of the actua worker
        file (str): File to be dispersed
        n (int): Number of chunks the file will be decomposed
        m (int): Number of chunks with the file could be composed
        field (int): Number used as a field. It is used by the algoritm to compute operations.

    Returns:
        str: Message of the execution status
    """
    sentence = './Dis '+str(n)+' '+str(m)+' '+str(field)+' ../../'+input_folder+'/'+file
    os.system(sentence)

    return 'dispersed file'


def recovery_file(wkr_id, file, m, field):
    """Recover file.

    Recover file with m chunks and its field.

    Args:
        wkr_id (str): Id of the actua worker
        file (str): File to be recovered
        m (int): Number of chunks with the file will be composed 
        field (int): Number used as a field. It is used by the algoritm to compute operations.

    Returns:
        str: Message of the execution status
    """
    dispersed_files = [x for x in os.listdir('./') if len(x) == 2]
    sentence = './Rec ' + file + ' ' + str(field)

    for i in range(0, m):
        sentence = sentence + ' ./' + dispersed_files[i]
    os.system(sentence)

    for k in dispersed_files:
        remove = 'rm ./' + k
        os.system(remove)

    return 'recovered file'


def run_pipeline(wid):
    """Function that runs pipeline with dispersal and recovery.

    Args:
        wid (str): Contains the id of the actual worker. In the form: SOL_ID-W_ID (ej: 1-1).

    Returns:
        bool: True if function done correctly False if not.
    """
    try:

        w_path = os.sep.join([home_path, output_folder, wid])
        create_subfolders(w_path,access_rights)
        w_p_dis = os.sep.join([w_path, dis])
        if not os.path.exists(w_p_dis):
            shutil.copyfile(dis, w_p_dis)
            os.system('chmod +x '+w_p_dis)

        w_p_rec = os.sep.join([w_path, rec])
        if not os.path.exists(w_p_rec):
            shutil.copyfile(rec, w_p_rec)
            os.system('chmod +x '+w_p_rec)

        os.chdir( w_path )
        print(os.getcwd())
        dispersal_file(wid,file1,N,M,FIELD)
        recovery_file(wid,file1,M,FIELD)

        ret = True
    except:
        ret = False

    return ret

def parseArguments():
    """
    define and parse arguments passed to the program
    """
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-r','--repeat', help='Desc', required=True)
    return parser.parse_args()



if __name__ == '__main__':
    args = parseArguments()
    
    i=1
    if int(args.repeat) > 0:
        while i <= int(args.repeat):
            print(f'i: {i}/{args.repeat}')
            print(f'BEGIN TEST ID:{ID}')
            rp = run_pipeline(ID)
            print(f'result: {rp}')
            print(f'END TEST ID:{ID}')
            i+=1
            time.sleep(1)
    elif int(args.repeat) == 0:
        while True:
            print(f'i: {i}/{args.repeat}')
            print(f'BEGIN TEST ID:{ID}')
            rp = run_pipeline(ID)
            print(f'result: {rp}')
            print(f'END TEST ID:{ID}')
            i+=1
            time.sleep(1)
    else:
        print('Error: value must be bigger than 0')
    