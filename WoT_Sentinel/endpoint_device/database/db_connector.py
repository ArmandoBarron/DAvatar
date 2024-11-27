import mysql.connector
import time 

time.sleep(30)

db = mysql.connector.connect(
  host = "db_service",
  user = "root",
  password = "secret",
  port = 3306,
  database = "scheme_info"
)
mycursor = db.cursor(buffered=True)

def insert_containers(id_container,name,status,image,volumes,platform,description,td_schema_pub,td_schema_priv,image_p,volumes_p,status_p):
  sql = "INSERT INTO containers (id_container,name,status,image,volumes,platform,description,td_scheme_pub,td_scheme_priv,image_p,volumes_p,status_p) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  val = (id_container,name,status,image,volumes,platform,description,td_schema_pub,td_schema_priv,image_p,volumes_p,status_p)
  mycursor.execute(sql,val)
  db.commit()
  #print(mycursor.rowcount, "record inserted.")

def insert_containers_utility(id_container,cpu_utility,memory_utility,network_utility,fs_utility,cpu_level,memory_level,network_level,fs_level,timestamp,utility_p):
  sql = "INSERT INTO containers_utility (id_container,cpu_utility,memory_utility,network_utility,fs_utility,cpu_level,memory_level,network_level,fs_level,timestamp_utility,utility_p) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  val = (id_container,cpu_utility,memory_utility,network_utility,fs_utility,cpu_level,memory_level,network_level,fs_level,timestamp,utility_p)
  mycursor.execute(sql,val)
  db.commit()
  #print(mycursor.rowcount, "record inserted.")

def insert_app(name,description,containers,td_schema):
  sql = "INSERT INTO applications (name,description,td_scheme) VALUES (%s,%s,%s)"
  td_schema = str(td_schema)
  print(td_schema)
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
  #print(mycursor.rowcount, "record inserted.")

def select_container_tdSchema(id_container):
  sql = "SELECT td_scheme_pub FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  td_schema = res[0]
  return td_schema

def select_container_tdSchema_priv(id_long):
  sql = "SELECT td_scheme_priv FROM containers WHERE id_long = %s"
  val = (id_long, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  td_schema = res[0]
  return td_schema

def select_container_info(id_container):
  sql = "SELECT name,status,image,volumes,entrypoint,platform,description,image_p,volumes_p,status_p FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchall()
  info = res[0]
  name = info[0]
  status = info[1]
  image = info[2]
  volumes = info[3]
  entrypoint = info[4]
  platform = info[5]
  description = info[6]
  image_p = info[7]
  volumes_p = info[8]
  status_p = info[9]
  sql = "SELECT cpu_utility,memory_utility,network_utility,fs_utility,cpu_level,memory_level,network_level,fs_level,timestamp_utility,utility_p FROM containers_utility WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res2 = mycursor.fetchall()
  info2 = res2[0]
  c_util = info2[0]
  m_util = info2[1]
  n_util = info2[2]
  f_util = info2[3]
  c_lvl = info2[4]
  m_lvl = info2[5]
  n_lvl = info2[6]
  f_lvl = info2[7]
  time = info2[8]
  utility_p = info2[9]
  return name,status,image,volumes,entrypoint,platform,description,image_p,volumes_p,status_p,c_util,m_util,n_util,f_util,c_lvl,m_lvl,n_lvl,f_lvl,time,utility_p

def select_container_info_priv(id_long):
  sql = "SELECT name,status,image,volumes,entrypoint,platform,description FROM containers WHERE id_long = %s"
  val = (id_long, )
  mycursor.execute(sql,val)
  res = mycursor.fetchall()
  info = res[0]
  name = info[0]
  status = info[1]
  image = info[2]
  volumes = info[3]
  entrypoint = info[4]
  platform = info[5]
  description = info[6]
  sql = "SELECT cpu_utility,memory_utility,network_utility,fs_utility,cpu_level,memory_level,network_level,fs_level,timestamp_utility FROM containers_utility WHERE id_long = %s"
  val = (id_long, )
  mycursor.execute(sql,val)
  res2 = mycursor.fetchall()
  info2 = res2[0]
  c_util = info2[0]
  m_util = info2[1]
  n_util = info2[2]
  f_util = info2[3]
  c_lvl = info2[4]
  m_lvl = info2[5]
  n_lvl = info2[6]
  f_lvl = info2[7]
  time = info2[8]
  return name,status,image,volumes,entrypoint,platform,description,c_util,m_util,n_util,f_util,c_lvl,m_lvl,n_lvl,f_lvl,time

def select_app_tdSchema(name):
  sql = "SELECT td_scheme FROM applications WHERE name = %s"
  val = (name, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  td_schema = res[0]
  return td_schema

def select_app_info(name):
  sql = "SELECT * FROM applications WHERE name = %s"
  val = (name, )
  mycursor.execute(sql,val)
  res = mycursor.fetchall()
  info = res[0]
  id_app = info[0]
  desc = info[2]
  sql2 = "SELECT id_container FROM applications_containers WHERE id_app = %s"
  val = (id_app, )
  mycursor.execute(sql2,val)
  res2 = mycursor.fetchall()
  conts = res2[0]
  names_cont = []
  for i in range(0,len(conts)):
    sql = "SELECT name FROM containers WHERE id_container = %s"
    val = (conts[i], )
    mycursor.execute(sql,val)
    res = mycursor.fetchone()
    names_cont.append(res[0])
  
  return names_cont,desc

def select_action_uri(name):
  sql = "SELECT URI FROM actions WHERE name = %s"
  val = (name, )
  mycursor.execute(sql,val)
  res = mycursor.fetchall()
  uri = res[0]
  return uri

def select_extra_uri(id_container,extra,type):
  sql = "SELECT name FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  sql = "SELECT URI FROM containers_extras WHERE name_container = %s AND extra = %s AND type = %s"
  val = (res[0],extra,type,)
  mycursor.execute(sql,val)
  res2 = mycursor.fetchone()
  return res2[0]

def select_container_port(id_container):
  sql = "SELECT docker_port FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  return res[0]

def select_user_pass(username):
  sql = "SELECT password FROM users WHERE username = %s"
  val = (username, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  return res[0]

def select_container_app(id_container):
  sql = "SELECT id_app FROM applications_containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  id_app = res[0]
  sql = "SELECT name FROM applications WHERE id_app = %s"
  val = (id_app, )
  mycursor.execute(sql,val)
  res2 = mycursor.fetchone()
  return res2[0]

def select_app_structure(name_app):
  sql = "SELECT structure_json FROM applications_graph WHERE name_app = %s"
  val = (name_app, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  return res[0]

def select_container_name(id_container):
  sql = "SELECT name FROM containers WHERE id_container = %s"
  val = (id_container, )
  mycursor.execute(sql,val)
  res = mycursor.fetchone()
  return res[0]

#hola
#print(select_app_info("small-app"))

#print(select_container_info_priv("ffdd03d65cc4c27afe1be213ccf7218088dc62adc9908359cb3e10fbdef5f257"))