# coding: utf-8
__author__ = 'ila'

from utils.configread import config_read
from utils.convert_mysql_to_hive import ConvertMySQLToHive
from utils.hive_func import hive_execute

dbtype, host, port, user, passwd, dbName, charset, _ = config_read("config.ini")

with open(f"./db/{dbName}.sql", encoding="utf-8") as f:
    raw_mysql = f.read()

cv = ConvertMySQLToHive(dbName)
hive_list = cv.convert_mysql_to_hive(raw_mysql)

hive_execute(hive_list)
