# coding:utf-8
__author__ = 'ila'

import os, configparser, sys, datetime

basedir = os.path.abspath(os.path.dirname(__file__))


# 开始从ini配置文件里导入参数


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "whatthefuck??????????"
    domain=''
    # sqlalchemy参数
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 自动commit
    SQLALCHEMY_PRE_PING = True
    SQLALCHEMY_POOL_SIZE = 0
    SQLALCHEMY_POOL_TIMEOUT = 100
    SQLALCHEMY_POOL_RECYCLE = 7200

    server_username = 'admin'
    server_password = '123456'
    HOST = '0.0.0.0'
    PORT = 8080


    cp = configparser.ConfigParser()

    cp.read('config.ini',encoding="utf-8")
    try:
        sql_type = cp.get("sql", "type")
    except:
        sql_type = "mysql"

    sql_host = cp.get("sql", "host")
    sql_port = int(cp.get("sql", "port"))
    sql_user = cp.get("sql", "user")
    sql_passwd = cp.get("sql", "passwd")
    sql_database =cp.get("sql", "db")
    sql_database=sql_database.lower()
    sql_charset=cp.get("sql", "charset")
    # 项目名称和版本
    project_name = u'py_shop'
    project_version = u'1.0'
    if sql_type == 'mysql':
        SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(
            sql_user, sql_passwd, sql_host, sql_port, sql_database
        )
    else:
        SQLALCHEMY_DATABASE_URI = "mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8".format(
            sql_user, sql_passwd, sql_host, sql_port, sql_database
        )
    # jwt参数
    JWT_AUTH_URL_RULE = '/user/login/'  # 跳转注册
    JWT_AUTH_HEADER_NAME = 'Authorization'
    JWT_SECRET_KEY = 'JSON-Web-Token-Projected-Every!!'
    JWT_EXPIRATION_DELTA = datetime.datetime.utcnow() + datetime.timedelta(days=7, seconds=0)  # token过期时间
    JWT_LEEWAY = 60
    JWT_DEFAULT_REALM = 'Login Required'
    JWT_ISS = 'shop.com'  # token签发者
    JWT_Algorithm = 'HS256'  # jwt加密算法

    SWAGGER = {
        "swagger": "2.0",
        'uiversion': "3",
        'title': 'py_flask项目接口文档(swagger规范)',
        "version": "1.0",
        'doc_dir': os.path.join(os.getcwd(), 'api/docs/'),
        "host": "{}:{}".format(HOST, PORT),
    }
    SWAGGER_TEMPLATE = {
        "schemes": ["http"],
        "securityDefinitions":
            {
                'JWT':
                    {
                        "description": "JWT授权(数据将在请求头中进行传输) 参数结构: “token: {token}”\n请在下面的value输入框输入:token",
                        'type': 'apiKey',
                        "name": "token",
                        "scheme": "token",

                        "in": "header"
                    }
            },
    }


class DevelopmentConfig(Config):
    threaded = True
    processes = 1
    DEBUG = True
    hostname = 'dev_server'

    TEST_HOST = 'py.shop.com'
    TEST_PORT = 8080
    PROTOCOL="http"



class OnLineConfig(Config):
    threaded = True
    processes=1
    DEBUG = True
    hostname = 'online_server'
    ws_ip = '127.0.0.1'
    ws_port = 8080
    PROTOCOL = "http"


configs = {
    'developmentConfig': DevelopmentConfig,
    'defaultConfig': DevelopmentConfig,
    'onlineConfig': OnLineConfig
}
