#coding:utf-8
__author__ = "ila"

def pyFileCheck(filename)->bool:
    '''
    check current file is or not py file
    :param filename:
    :return:
    '''
    if type(filename)!=type(""):
        return False
    if filename[-3:]==".py":
        return True
    else:
        return False