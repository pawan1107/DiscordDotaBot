import pymongo
try:
  import dnspython
except ModuleNotFoundError:
  print("")
  
  
myclient = pymongo.MongoClient("mongodb+srv://Pawan:Pawan1107@user.we9ez.mongodb.net/user?retryWrites=true&w=majority")

userDB = myclient["user"]


def insertExample():
  
  userDB.insertone({"id":1, "name": "Pawan"})

  print(userDB.find({"name": "Pawan"}))