#!/usr/bin/python3
# Execution command: python3 generate-files.py -s 100M -n 64 -p ~/prototype/solutions/kulla/volume/Source
# Execution command: python3 generate-files.py -s 200M -n 32 -p ~/prototype/solutions/kulla/volume/Source
# Execution command: python3 generate-files.py -s 200M -n 2 -p ~/prototype/solutions/kulla/MasterSlave/volume/Source

import os
import argparse


access_rights = 0o777

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
        print('Creation of the directory failed')
        print(path)
    return cr

def parseArguments():
    """
    define and parse arguments passed to the program
    """
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-s','--sizefile', help='Desc', required=True)
    parser.add_argument('-n','--nfiles', help='Desc', required=True)
    parser.add_argument('-p','--path', help='Desc', required=True)
    return parser.parse_args()

if __name__ == '__main__':
    args = parseArguments()
    create_subfolders(args.path,access_rights)

    for i in range(1,int(args.nfiles)+1):
        filename = '{}_{}.txt'.format(args.sizefile, str(i))
        path_file = os.sep.join([args.path, filename])
        if not os.path.exists(path_file):
            # 'head -c 1G </dev/urandom >myfile'
            command = 'head -c {} </dev/urandom > {}'.format(args.sizefile, path_file)
            print(command)
            cm = os.system(command)
        else:
            print('File already exists')
    