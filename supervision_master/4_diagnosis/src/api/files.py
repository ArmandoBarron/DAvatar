import os
import pandas as pd
import json

def make_subfolders(path, access_rights=0o665):
  """Make directories recursively with access rights.
  Args:
    path (str): path to folder
    access_rights (int, optional): access rights to apply recursively. Defaults to 0o665.
  Returns:
    bool: true if directory created false if not.
  """
  cr = False
  try:
    if not os.path.exists(path):
      os.makedirs(path, access_rights)
      cr = True
  except OSError:
    print ('Make directory failed: ', path)
  return cr

def write_json_to_disk(jsond, filename):
  if jsond and filename:
    with open(filename, 'w') as f:
      f.write("%s" % json.dumps(jsond))
    print(f'File saved: {filename}')

def export_to_csv(filename, data, flag_idx=False):
    """save data to csv file

    Args:
        filename (str): the filename to save with
        data (object): could be [dict | list | pd.DataFrame]
        flag_idx (bool): define if save file with the index numbers

    Returns:
        int: 1 if saved -1 if not
    """
    filename = (filename if '.csv' in filename else filename+'.csv')
    saved = 0
    try:
        if data is dict:
            df = pd.read_json(data)
        elif data is list:
            df = pd.DataFrame(data)
        else:
            df = data

        # print(df.keys())
        # print(df.head())
        # print(df.shape)
        # print(df.describe())

        not_svd = df.to_csv(filename, index=flag_idx)
        if not not_svd:
            saved = 1
            print('File saved: '+filename)
        else:
            saved = -1
    except:
        print('Error saving csv: '+filename)
        saved = -1

    return saved
