import hashlib
import database.db_connector

def getInfoUser():
    username = input("\nUsername: ")
    password = input("\nPassword: ")
    return username,password

def protectPass(password):
    protectPass = hashlib.md5(password.encode())
    pp = protectPass.hexdigest()
    return pp

def storeValuesUser(username,password,admin):
    database.db_connector.insert_user(username,password,admin)

username, password = getInfoUser()
pp = protectPass(password)
storeValuesUser(username,pp,admin=1)
