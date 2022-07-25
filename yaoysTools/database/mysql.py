# -*- coding: UTF-8 -*-
"""
    作者: 小肥巴巴
    简书: https://www.jianshu.com/u/db796a501972
    邮箱: imyunshi@163.com
    github: https://github.com/xiaofeipapa/python_example
    您可以任意转载, 恳请保留我作为原作者, 谢谢.

    2022-4-21
    yaoys 在原作者代码的基础上进行优化修改
"""
from timeit import default_timer

import pymysql
import pymysql.cursors
from dbutils.pooled_db import PooledDB


class DMysqlConfig:
    """

        :param mincached:连接池中空闲连接的初始数量
        :param maxcached:连接池中空闲连接的最大数量
        :param maxshared:共享连接的最大数量
        :param maxconnections:创建连接池的最大数量
        :param blocking:超过最大连接数量时候的表现，为True等待连接数量下降，为false直接报错处理
        :param maxusage:单个连接的最大重复使用次数
        :param setsession:optional list of SQL commands that may serve to prepare
            the session, e.g. ["set datestyle to ...", "set time zone ..."]
        :param reset:how connections should be reset when returned to the pool
            (False or None to rollback transcations started with begin(),
            True to always issue a rollback for safety's sake)
        :param host:数据库ip地址
        :param port:数据库端口
        :param db:库名
        :param user:用户名
        :param passwd:密码
        :param charset:字符编码
    """

    def __init__(self, host, db, user, password, port):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password

        self.charset = 'UTF8'  # 不能是 utf-8
        self.minCached = 10
        self.maxCached = 20
        self.maxShared = 10
        self.maxConnection = 100

        self.blocking = True
        self.maxUsage = 100
        self.setSession = None
        self.reset = True


# ---- 用连接池来返回数据库连接
class DMysqlPoolConn:
    __pool = None

    def __init__(self, config):
        if not self.__pool:
            self.__class__.__pool = PooledDB(creator=pymysql,
                                             maxconnections=config.maxConnection,
                                             mincached=config.minCached,
                                             maxcached=config.maxCached,
                                             maxshared=config.maxShared,
                                             blocking=config.blocking,
                                             maxusage=config.maxUsage,
                                             setsession=config.setSession,
                                             charset=config.charset,
                                             host=config.host,
                                             port=config.port,
                                             database=config.db,
                                             user=config.user,
                                             password=config.password,
                                             )

    def get_conn(self):
        return self.__pool.connection()


# ---- 用pymysql 操作数据库
def get_connection(host, port, db, user, password):
    db_config = DMysqlConfig(host, db, user, password, port)
    g_pool_connection = DMysqlPoolConn(db_config)
    conn = g_pool_connection.get_conn()
    return conn


# ---- 使用 with 的方式来优化代码
class UsingMysql(object):

    def __init__(self, host, port, dbname, username, password, commit=True, log_time=True, log_label='总用时'):
        """

        :param commit: 是否在最后提交事务(设置为False的时候方便单元测试)
        :param log_time:  是否打印程序运行总时间
        :param log_label:  自定义log的文字
        :param host: 数据库ip地址
        :param port: 端口号
        :param dbname: 库名
        :param username: 数据库用户名
        :param password: 数据库密码
        """
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label
        self._host = host
        self._port = port
        self._dbname = dbname
        self._username = username
        self._password = password

    def __enter__(self):

        # 如果需要记录时间
        if self._log_time is True:
            self._start = default_timer()

        # 在进入的时候自动获取连接和cursor
        conn = get_connection(self._host, self._port, self._dbname, self._username, self._password)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        conn.autocommit = False

        self._conn = conn
        self._cursor = cursor
        return self

    def __exit__(self, *exc_info):
        # 提交事务
        if self._commit:
            self._conn.commit()
        # 在退出的时候自动关闭连接和cursor
        self._cursor.close()
        self._conn.close()

        if self._log_time is True:
            diff = default_timer() - self._start
            print('-- %s: %.6f 秒' % (self._log_label, diff))

    # 查找一条数据
    def fetch_one(self, sql, params=None):
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    # 查找所有数据
    def fetch_all(self, sql, params=None):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    # 根据id获取数据
    def fetch_by_pk(self, sql, pk):
        self.cursor.execute(sql, (pk,))
        return self.cursor.fetchall()

    # 根据参数更新数据
    def update_all(self, sql, params=None):
        self.cursor.execute(sql, params)

    # 根据参数删除数据
    def delete_all(self, sql, params=None):
        self.cursor.execute(sql, params)

    @property
    def cursor(self):
        return self._cursor


"""
以下为测试
"""


def delete_one(cursor, name):
    sql = 'delete from user where name = %s'
    params = name
    cursor.execute(sql, params)
    print('--- 已删除名字为%s. ' % name)


def select_one(cursor):
    sql = 'select * from user'
    cursor.execute(sql)
    return cursor.fetchone()


def update_by_pk(cursor, name, pk):
    sql = "update user set name = '%s' where id = %d" % (name, pk)

    cursor.execute(sql)


# 修改记录
def check_update(cursor):
    # 查找一条记录
    data = select_one(cursor)
    pk = data['id']
    print('--- {0}: '.format(data))

    # 修改名字
    new_name = 'aaaa'
    update_by_pk(cursor, new_name, pk)

    # 查看
    select_one_by_name(cursor, new_name)


def select_one_by_name(cursor, name):
    sql = 'select * from user where name = %s'
    params = name
    cursor.execute(sql, params)
    data = cursor.fetchone()
    if data:
        print('--- 已找到名字为%s. ' % data['name'])
    else:
        print('--- 名字为%s的已经没有了' % name)


if __name__ == '__main__':
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
