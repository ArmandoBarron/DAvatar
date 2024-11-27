import os
import json
from .constants import FLAG_SAVE_DATASETS

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
    print('Make directory failed: ', path)
  return cr

def write_jsons_to_disk(all_tds, filename):
  if all_tds and FLAG_SAVE_DATASETS:
    with open(filename, 'w') as f:
      for td in all_tds:
        if td:
          f.write("%s\n" % json.dumps(td))
    print(f'File saved: {filename}')