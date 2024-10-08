# coding:utf-8
# author:ila
import click,py_compile,os
from configparser import ConfigParser
from configs import configs
from utils.mysqlinit import Create_Mysql
from api import create_app
from api.exts import db
from api.models.user_model import *
from api.models.config_model import *
from api.models.brush_model import *
@click.group()
def sub():
    pass


@click.command()
@click.option("-v", default=0.1, type=float)
def verr(v):
    # VERSION = 0.1
    click.echo("py sub system version:{}".format(v))


@click.command()
def run():
    app = create_app(configs)
    app.debug = configs['defaultConfig'].DEBUG
    app.run(
        host=configs['defaultConfig'].HOST,
        port=configs['defaultConfig'].PORT,
        threaded=configs['defaultConfig'].threaded,
        processes=configs['defaultConfig'].processes
    )


@click.command()
def create_all():
    app = create_app(configs)
    with app.app_context():
        print("creat_all")
        db.create_all()

@click.command()
@click.option("--ini", type=str)
def initsql(ini):
    cp = ConfigParser()
    cp.read(ini,encoding="utf-8")
    sqltype = cp.get("sql", "type")
    database= cp.get("sql", "db")
    if sqltype == 'mysql':
        cm = Create_Mysql(ini)
        cm.create_db("CREATE DATABASE IF NOT EXISTS  `{}`  /*!40100 DEFAULT CHARACTER SET utf8 */ ;".format(database))
        with open("./db/mysql.sql", encoding="utf8") as f:
            createsql = f.read()
        createsql = "DROP TABLE" + createsql.split('DROP TABLE', 1)[-1]
        cm.create_tables(createsql.split(';\n')[:-1])
        cm.conn_close()
    elif sqltype == 'mssql':
        cm = Create_Mysql(ini)
        cm.create_db("CREATE DATABASE IF NOT EXISTS  `{}` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;".format(database))
        with open("./db/mssql.sql", encoding="utf8") as f:
            createsql = f.read()
        createsql = "DROP TABLE" + createsql.split('DROP TABLE', 1)[-1]
        cm.create_tables(createsql.split(';\n')[:-1])
        cm.conn_close()
    else:
        print('请修改当前面目录下的config.ini文件')

@click.command()
@click.option("--py_path", type=str)
def compile(py_path):
    print("py_path====>",py_path)
    py_compile.compile(py_path)


@click.command()
def replace_admin():
    filePath=os.path.join(os.getcwd(),"api/templates/front/index.html")
    if os.path.isfile(filePath):
        print(filePath)
        with open(filePath,"r",encoding="utf-8") as f:
            datas=f.read()
        datas=datas.replace('baseurl+"admin/dist/index.html#"','"http://localhost:8080/admin"')
        datas=datas.replace('baseurl+"admin/dist/index.html#/login"','"http://localhost:8080/admin"')

        with open(filePath,"w",encoding="utf-8") as f:
            f.write(datas)


sub.add_command(verr)
sub.add_command(run,"run")
sub.add_command(create_all,"create_all")
sub.add_command(initsql,"initsql")
sub.add_command(replace_admin,"replace_admin")
if __name__ == "__main__":
    sub()
