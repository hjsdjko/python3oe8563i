#coding:utf-8
__author__ = "ila"

from configs import configs
from api import create_app
app = create_app(configs)
app.debug = configs['defaultConfig'].DEBUG
app.run(
    host=configs['defaultConfig'].HOST,
    port=configs['defaultConfig'].PORT,
    threaded=configs['defaultConfig'].threaded,
    processes=configs['defaultConfig'].processes
)
