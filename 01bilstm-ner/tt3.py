import pymongo
myclient=pymongo.MongoClient(host='127.0.0.1',port=27017)   #指定主机和端口号创建客户端
mydb=myclient['dbtest']#数据库使用
mycol=mydb['t1']