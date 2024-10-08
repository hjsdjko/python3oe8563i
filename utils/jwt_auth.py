# coding:utf-8
# author:ila
import base64, copy
from flask import jsonify, session, request

from api.models.models import Base_model

from utils.codes import *

class Auth(object):
    def authenticate(self, model, req_dict):
        """
        用户登录，登录成功返回token；登录失败返回失败原因
        :param username:账号
        :param password:密码
        :return: json
        """
        msg = {'code': normal_code, 'message': 'success', 'data': {}}
        tablename=model.__tablename__
        encode_dict = {"tablename":tablename, "params": req_dict}

        encode_str = base64.b64encode(str(encode_dict).encode("utf8"))
        msg['data']['id']=req_dict.get("id")
        msg['id']=req_dict.get("id")
        msg['token'] = encode_str.decode('utf-8')
        return jsonify(msg)

    def get_token(self, model, req_dict):
        tablename=model.__tablename__
        encode_dict = {"tablename":tablename, "params": req_dict}

        encode_str = base64.b64encode(str(encode_dict).encode("utf8"))
        return encode_str.decode('utf-8')

    def identify(self, request):
        """
        用户鉴权
        :param request:本次请求对象
        :return: list
        """

        msg = {'code': normal_code, 'message': 'success', 'data': {}}
        auth_header = request.headers.get('token')
        if auth_header:

            auth_token = copy.deepcopy(auth_header)

            decode_str = base64.b64decode(auth_token).decode("utf8")

            decode_dict = eval(decode_str)

            tablename2 = decode_dict.get("tablename")

            params2 = decode_dict.get("params")


            mapping_str_to_object = {}
            for model in Base_model._decl_class_registry.values():
                if hasattr(model, '__tablename__'):
                    mapping_str_to_object[model.__tablename__] = model
            datas = mapping_str_to_object[tablename2].getbyparams(
                mapping_str_to_object[tablename2],
                mapping_str_to_object[tablename2],
                params2
            )
            if not datas:
                msg['code'] = username_error_code
                msg['msg'] = '找不到该用户信息'
                result = msg
            else:
                session['tablename'] = tablename2
                session['params'] = params2
                msg['msg'] = '身份验证通过。'
                result = msg
        else:
            msg['code'] = 401
            msg['message'] = 'headers未包含认证信息。'
            result = msg
        return result
