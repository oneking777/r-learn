#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from . import api
from flask import request, jsonify, current_app, session
from ihome import redis_store, db
from ihome.models import User
from ihome import constants
from ihome.utils.response_code import RET
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash


# api/v1.0/users
@api.route("/users", methods=["POST"])
def register():
    """注册
    请求的参数：手机号，短信验证码，密码, 确认密码
    参数格式：json
    :return:
    """
    # 获取请求的json数据
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    sms_code = req_dict.get("sms_code")
    password = req_dict.get("password")
    password2 = req_dict.get("password2")

    # 校验参数
    if not all([mobile, sms_code, password, password2]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 判断手机号格式
    if not re.match(r"1[34578]\d{9}", mobile):
        # 表示格式不对
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式错误")

    # 校验二次密码
    if password != password2:
        return jsonify(errno=RET.PARAMERR, errmsg="两次密码不一致")

    # 业务处理
    # 从redis中取出短信验证码
    try:
        real_sms_code = redis_store.get("sms_code_%s" % mobile)
    except Exception as e:
        # current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="读取真实短信验证码异常")

    # 判断短信验证码是否过期
    if real_sms_code is None:
        return jsonify(errno=RET.NODATA, errmsg="短信验证码已失效")

    # 删除redis中短信验证码，防止重复使用
    try:
        redis_store.delete("sms_code_%s" % mobile)
    except Exception as e:
        # current_app.logger.error(e)
        pass

    # 判断用户填写的短信验证码是否正确
    if real_sms_code != sms_code:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码错误")

    # 判断用户的手机号是否被注册过
    # try:
    #     user = User.query.filter_by(mobile=mobile).first()
    # except Exception as e:
    #     # current_app.logger.error(e)
    #     return jsonify(errno=RET.DBERR, errmsg="数据库异常")
    # else:
    #     if user is not None:
    #         # 手机号已存在
    #         return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

    # 保存注册数据到数据库中
    user = User(name=mobile, mobile=mobile)
    # user.generate_password_hash(password)

    user.password = password  # 设置属性

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        # 数据库操作错误后的回滚
        db.session.rollback()
        # 表示手机号出现了重复值，即手机号已存在
        # current_app.logger.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
    except Exception as e:
        db.session.rollback()
        # current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="查询数据库异常")

    # 保存登录状态到session中
    session["name"] = mobile
    session["mobile"] = mobile
    session["user_id"] = user.id

    return jsonify(errno=RET.OK, errmsg="注册成功")


# /api/v1.0/sessions
@api.route("/sessions", methods=["POST"])
def login():
    """用户登录
    :param 手机号，密码 ：json
    """
    # 前端接受数据
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    password = req_dict.get("password")

    # 校验数据
    # 校验数据完整性
    if not all([mobile, password]):
        return jsonify(errno=RET.DATAERR, errmsg="数据不完整")

    # 校验手机格式
    if not re.match(r"1[34578]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式不正确")

    # 判断错误次数是否超过限制，如果超过限制，则返回
    # redis记录： "access_nums_请求ip地址": 次数
    user_ip = request.remote_addr  # 用户ip
    try:
        access_nums = redis_store.get("access_nums_%s" % user_ip)
    except Exception as e:
        # current_app.logger.error(e)
        pass
    else:
        if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg="错误次数过多，请稍后重试")

    # 从数据库中查询手机号对象
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        # current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息错误")

    # 用户名和密码一起校验
    if user is None or not user.check_password(password):
        # 如果验证失败，记录错误次数
        try:
            redis_store.incr("access_nums_%s" % user_ip)
            redis_store.expire("access_nums_%s" % user_ip, constants.LOGIN_ERROR_FORBID_TIMES)
        except Exception as e:
            current_app.logger.error(e)
            pass
        return jsonify(errno=RET.DATAERR, errmsg="用户名或密码错误")

    # 记录用户登录状态
    session["name"] = user.name
    session["mobile"] = user.mobile
    session["user_id"] = user.id

    return jsonify(errno=RET.OK, errmsg="登录成功")


@api.route("/session", methods=["GET"])
def check_login():
    """
    检查登录状态
    :return:
    """
    # 尝试从session中获取信息
    name = session.get("name")
    # 如果用户已登陆，则返回用户名，否则返回None
    if name is not None:
        return jsonify(errno=RET.OK, errmsg="true", data={"name": name})
    else:
        return jsonify(errno=RET.SESSIONERR, errmsg="false")


@api.route("/session", methods=["DELETE"])
def logout():
    """用户退出"""
    # 清除用户session信息
    csrf_token = session.get("csrf_tokrn")
    session.clear()
    session["csrf_tokrn"] = csrf_token
    return jsonify(errno=RET.OK, errmsg="ok")
