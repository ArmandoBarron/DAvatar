from Crypto.Hash import SHA3_256

def get_SHA3_256(data):
  """Get the hex sha3 representation of a string.

  Args:
      data (str): string to get its hash

  Returns:
      str: hex hash representation
  """
  bytes_data = bytes(data, 'utf-8')
  h_obj = SHA3_256.new()
  h_obj.update(bytes_data) #b'Some data'
  return h_obj.hexdigest()