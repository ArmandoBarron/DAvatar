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

def insert_user(username,password,admin):
  sql = "INSERT INTO users (username,password,admin) VALUES (%s,%s,%s)"
  val = (username,password,admin)
  mycursor.execute(sql,val)
  db.commit()

#print(select_container_tdSchema("e35bea536b4b"))