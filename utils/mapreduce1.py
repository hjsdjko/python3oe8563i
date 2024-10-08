# coding: utf-8
__author__ = 'ila'
import configparser
from mrjob.job import MRJob
import pymysql

cp = configparser.ConfigParser()
cp.read('config.ini',encoding="utf-8")
host=cp.get('sql','host')
user=cp.get('sql','user')
passwd=cp.get('sql','passwd')
dbName=cp.get('sql','db')
class MRMySQLAvg(MRJob):

    def mapper_init(self):
        # 连接数据库
        self.conn = pymysql.connect(host=host, user=user, passwd=passwd, db=dbName)
        self.cursor = self.conn.cursor()

    def mapper(self, _,sql):
        # 从数据库中读取一行数据
        self.cursor.execute(sql)
        datas = self.cursor.fetchone()

        # 将数据传递给reducer
        yield datas

    def mapper_final(self):
        # 关闭数据库连接
        self.cursor.close()
        self.conn.close()

    def reducer(self):
        data_dict = [[row[0],row[1]] for row in self.cursor.fetchall()]
        yield data_dict

if __name__ == '__main__':
    MRMySQLAvg.run()