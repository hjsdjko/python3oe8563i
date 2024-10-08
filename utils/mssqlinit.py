#coding:utf-8
import os,sys,logging
from configparser import ConfigParser
import pymssql

class Create_Mssql(object):
    def __init__(self, inipath):
        if not os.path.isfile(inipath):
            logging.warning("ini is not exist : {}".format(inipath))
            sys.exit()

        cp = ConfigParser()
        cp.read(inipath)

        host = cp.get("sql", "host")
        port = int(cp.get("sql", "port"))
        user = cp.get("sql", "user")
        passwd = cp.get("sql", "passwd")
        self.db = cp.get("sql", "db")
        charset = cp.get("sql", "charset")
        self.conn = pymssql.connect(host=host, user=user, passwd=passwd, port=port, charset=charset)
        self.cur = self.conn.cursor()

    def create_db(self, sql):
        self.cur.execute(sql)
        self.conn.commit()

    def create_tables(self, sqls):
        use_sql = '''use `{}`;'''.format(self.db)
        self.cur.execute(use_sql)

        for sql in sqls:
            self.cur.execute(sql)
            self.conn.commit()

    def conn_close(self):
        self.cur.close()
        self.conn.close()
