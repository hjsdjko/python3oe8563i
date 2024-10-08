#coding:utf-8
from configparser import ConfigParser
import logging,sys,os
import pymysql

class Create_Mysql(object):
    def __init__(self,inipath):
        if not os.path.isfile(inipath):
            logging.warning("ini is not exist : {}".format(inipath))
            sys.exit()

        cp=ConfigParser()
        cp.read(inipath,encoding="utf-8")

        host=cp.get("sql","host")
        port=int(cp.get("sql","port"))
        user=cp.get("sql","user")
        passwd=cp.get("sql","passwd")
        self.db=cp.get("sql","db")
        charset=cp.get("sql","charset")
        self.conn = pymysql.connect(host=host, user=user, passwd=passwd, port=port, charset=charset)
        self.cur = self.conn.cursor()
    def create_db(self,sql):
        self.cur.execute(sql)
        self.conn.commit()
    def create_tables(self,sqls):
        use_sql = '''use `{}`;'''.format(self.db)
        self.cur.execute(use_sql)


        for sql in sqls:
            try:
                self.cur.execute(sql)
                self.conn.commit()
            except Exception as e:
                print(e)



    def conn_close(self):
        self.cur.close()
        self.conn.close()
