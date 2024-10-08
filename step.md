1，解压项目zip包
2，阅读readme.md文件
3，安装项目需要的包 pip install -r requirements.txt
4，修改项目文件夹里的config.ini配置文件内容
5，运行命令初始化数据库  python manage.py initsql --ini config.ini
6，运行命令初始化所有表 python manage.py create_all
7，启动 python manage.py run