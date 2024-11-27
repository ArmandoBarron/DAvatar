import mysql.connector

db = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "secret",
  port = 33061,
  database = "scheme_info",
  auth_plugin='mysql_native_password'
)
mycursor = db.cursor(buffered=True)

def insert_containers(id_container,id_long,name,status,image,volumes,platform,description,td_schema):
  sql = "INSERT INTO containers (id_container,id_long,name,status,image,volumes,platform,description,td_scheme) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  val = (id_container,id_long,name,status,image,volumes,platform,description,td_schema)
  mycursor.execute(sql,val)
  db.commit()
  print(mycursor.rowcount, "record inserted.")

def insert_containers_utility(id_container,id_long,cpu_utility,memory_utility,network_utility,fs_utility,cpu_level,memory_level,network_level,fs_level,timestamp,utility_p):
  sql = "INSERT INTO containers_utility (id_container,id_long,cpu_utility,memory_utility,network_utility,fs_utility,cpu_level,memory_level,network_level,fs_level,timestamp_utility,utility_p) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  val = (id_container,id_long,cpu_utility,memory_utility,network_utility,fs_utility,cpu_level,memory_level,network_level,fs_level,timestamp,utility_p)
  mycursor.execute(sql,val)
  db.commit()
  print(mycursor.rowcount, "record inserted.")

def insert_app(name,description,containers,td_schema):
  sql = "INSERT INTO applications (name,description,td_scheme) VALUES (%s,%s,%s)"
  td_schema = str(td_schema)
  val = (name,description,td_schema)
  mycursor.execute(sql,val)
  db.commit()

  sql = "SELECT id_app FROM applications WHERE name = %s"
  val = (name, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  id_app = res[0]
  for i in range(0,len(containers)):
    insert_app_containers(id_app,containers[i])

def insert_app_containers(id_app,id_container):
  sql = "INSERT INTO applications_containers (id_app,id_container) VALUES (%s,%s)"
  val = (id_app,id_container)
  mycursor.execute(sql,val)
  db.commit()
  print(mycursor.rowcount, "record inserted.")

def select_container_tdSchema(id_container):
  sql = "SELECT td_scheme FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  td_schema = res[0]
  return td_schema

def select_container_info(id_container):
  sql = "SELECT name,status,image,volumes,platform,description FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchall()
  info = res[0]
  name = info[0]
  status = info[1]
  image = info[2]
  volumes = info[3]
  platform = info[4]
  description = info[5]
  return name,status,image,volumes,platform,description

def select_container_name(id_container):
  sql = "SELECT name FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  name = res[0]
  return name

def select_container_status(id_container):
  sql = "SELECT status FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  status = res[0]
  return status

def select_container_image(id_container):
  sql = "SELECT image FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  image = res[0]
  return image

def select_container_volumes(id_container):
  sql = "SELECT volumes FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  volumes = res[0]
  return volumes

def select_container_platform(id_container):
  sql = "SELECT platform FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  platform = res[0]
  return platform

def select_container_description(id_container):
  sql = "SELECT description FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  description = res[0]
  return description

def update_container_status(id_container,status):
  sql = "UPDATE containers SET status = %s WHERE id_container = %s"
  val = (status,id_container)
  mycursor.execute(sql,val)
  db.commit()

def select_all_names():
  sql = "SELECT id_container,id_long,name FROM containers"
  mycursor.execute(sql)
  res = mycursor.fetchall()
  names = res
  return names

def select_all_names_app():
  sql = "SELECT id_app,name FROM applications"
  mycursor.execute(sql)
  res = mycursor.fetchall()
  names = res
  return names

def select_containers_utility(id_container):
  sql = "SELECT * FROM containers_utility WHERE id_container = %s ORDER BY timestamp_utility DESC LIMIT 1"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  utility = res
  return utility

def select_all_status(id_app):
  sql = "SELECT id_container FROM applications_containers WHERE id_app = %s"
  val = (id_app, )
  mycursor.execute(sql,val)
  res = mycursor.fetchall()
  containers = res
  status = []
  for i in range(0,len(containers)):
    sql = "SELECT status FROM containers WHERE id_container = %s"
    val = (containers[i][0],)
    mycursor.execute(sql,val)
    res2 = mycursor.fetchone()
    status.append(res2)
  return status,containers

def select_container_rows(id_container):
  sql = "SELECT utility_p FROM containers_utility WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchall()
  return res

def select_container_id(name):
  sql = "SELECT id_container,id_long,status FROM containers WHERE name = %s"
  val = (name, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  id_container = res[0]
  id_long = res[1]
  status = res[2]
  return id_container,id_long,status

def select_app_graph(name):
  sql = "SELECT EXISTS(SELECT * FROM applications_graph WHERE name_app = %s)"
  val = (name, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  return res

def insert_app_graph(name,structure_json,status_json):
  sql = "INSERT INTO applications_graph (name_app,structure_json,status_json) VALUES (%s,%s,%s)"
  val = (name,structure_json,status_json)
  mycursor.execute(sql,val)
  db.commit()

def update_app_graph(name,status_json):
  sql = "UPDATE applications_graph SET status_json = %s WHERE name_app = %s"
  val = (status_json,name)
  mycursor.execute(sql,val)
  db.commit()

#print(select_all_status("4"))
