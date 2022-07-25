from yaoysTools.database.mysql import UsingMysql

host = 'localhost'
port = 3306
db = 'test'
user = 'root'
password = '123456'
with UsingMysql(host=host, port=port, dbname=db, username=user, password=password, log_time=True) as um:
    um.cursor.execute("select count(id) as total from user")
    data = um.cursor.fetchone()
    print("-- 当前数量: %d " % data['total'])

    um.cursor.execute("select * from user")
    data = um.cursor.fetchone()
    print("-- 单条记录: {0} ".format(data))

with UsingMysql(host=host, port=port, dbname=db, username=user, password=password, log_time=True) as um:
    sql = "insert into user(name, age) values(%s, %s)"
    params = ("user111", 25)
    um.cursor.execute(sql, params)

    um.cursor.execute("select * from user")
    data = um.cursor.fetchall()
    print("-- 记录: {0} ".format(data))
