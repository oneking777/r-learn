#!/usr/bin/env python
# -*- coding: utf-8 -*-


from werkzeug.routing import BaseConverter
from flask import session, jsonify, g
from ihome.utils.response_code import RET
import functools


class ReConverter(BaseConverter):
    """定义正则转换器"""
    def __init__(self, url_map, regx):
        # 调用父类方法
        super(ReConverter, self).__init__(url_map)
        # 保存正则表达式
        self.regex = regx


# 自定义验证登录状态的装饰器
def login_required(view_func):

    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # 判断用户登录状态
        # 如果用户是登录的，执行视图函数
        user_id = session.get("user_id")
        if user_id is not None:
            # 将user_id保存到g对象中，在视图函数中可以通过g对象获得保存的数据
            g.user_id = user_id
            return view_func(*args, **kwargs)
        else:
            # 如果未登录，返回未登录信息
            return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")

    return wrapper

