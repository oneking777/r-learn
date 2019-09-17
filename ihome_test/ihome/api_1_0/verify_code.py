# coding:utf-8


from . import api
import random
from ihome.utils.captcha.captcha import captcha
from ihome.tasks.sms.tasks import send_sms
from ihome import constants, db, redis_store
from flask import current_app, jsonify, make_response, request
from ihome.utils.response_code import RET
from ihome.models import User


# GET 127.0.0.1/api/v1.0/image_codes/<image_code_id>
@api.route("/image_codes/<image_code_id>")
def get_image_code(image_code_id):
    """
    获取前端验证码图片
    :param image_code_id: 图片验证码编号
    :return: 正常：验证码图片， 异常：返回json
    """
    # 获取参数
    # 校验参数
    # 业务逻辑处理
    #  生成验证码图片
    # 名字，真是文本，图片数据
    name, text, image_data = captcha.generate_captcha()

    #  将验证码真实值和编号保存到redis中,设置有效期
    # redis:   字符串   列表    哈希   set    zset
    #  "key": xxx
    # 采用哈希维护有效期时，只能整体设置
    #  "image_codes": {"":"", "":""}  哈希  hset("image_codes", "id1", "abc")

    # 单条维护记录，选用字符串类型
    # "image_code_编号": "真是文本值"
    # redis_store.set("image_code_%s" % image_code_id, text)
    # redis_store.expire("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES)
    #                    记录名字                               有效期                        记录文本
    try:
        redis_store.setex("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        # 捕获异常，记录日志
        # current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="save image code id failed")

    # 返回值
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp


# # GET /api/v1.0/sms_codes/<mobile>?image_code=xxx&image_code_id=xxx
# @api.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
# def get_sms_code(mobile):
#     """获取短信验证码"""
#     # 获取参数
#     image_code = request.args.get("image_code")
#     image_code_id = request.args.get("image_code_id")
#
#     # 校验参数
#     if not all([image_code, image_code_id]):
#         # 表示参数不完整
#         return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
#
#     # 业务逻辑处理
#     # 从redis中取出真是图片验证码
#     try:
#         # 有值则返回，无值则返回None
#         real_image_code = redis_store.get("image_code_%s" % image_code_id)
#     except Exception as e:
#         # current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR, errmsg="redis数据库异常")
#
#     # 删除图片验证码，防止用户使用同一个图片验证多次
#     try:
#         redis_store.delete("image_code_%s" % image_code_id)
#     except Exception as e:
#         # current_app.logger.error(e)
#         pass
#
#     # 判断图片验证码是否过期
#     if real_image_code is None:
#         # 图片验证码已过期
#         return jsonify(errno=RET.NODATA, errmsg="图片验证码已过期")
#
#     # 与用户填写的值进行对比
#     if real_image_code.lower() != image_code.lower():
#         # 用户填写错误
#         return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")
#
#     # 判断对于这个手机号的操作在60秒内有没有之前的记录，如果有，则认为操作频发，不予处理
#     try:
#         send_flag = redis_store.get("sms_code_%s" % mobile)
#     except Exception as e:
#         # current_app.logger.error(e)
#         pass
#     else:
#         if send_flag is not None:
#             # 表示在60秒内有过之前的记录
#             return jsonify(errno=RET.REQERR, errmsg="请求过于频繁，请60秒后再试")
#
#     # 判断手机号是否存在
#     # 有则为对象，无则返回None
#     try:
#         user = User.query.filter_by(mobile=mobile).first()
#     except Exception as e:
#         # current_app.logger.error(e)
#         pass
#     else:
#         if user is not None:
#             # 手机号已存在
#             return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
#
#     # 如果手机号不存在，则生成短信验证码
#     sms_code = "%06d" % random.randint(0, 999999)
#
#     # 保存真实的短信验证码
#     try:
#         redis_store.setex("sms_code_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
#         # 保存发送给这个手机号的记录，防止用户在60秒内再次出现发送短信的操作
#         redis_store.setex("send_sms_code_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
#     except Exception as e:
#         # current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR, errmsg="redis数据库异常")
#
#     # 发送短信
#     try:
#         ccp = CCP()
#         result = ccp.send_template_sms(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES/60)], 1)
#     except Exception as e:
#         # current_app.logger.error(e)
#         return jsonify(errno=RET.THIRDERR, errmsg="发送异常")
#
#     if result == 0:
#         # 表示发送成功
#         return jsonify(errno=RET.OK, errmsg="发送成功")
#     else:
#         # 发送不成功
#         return jsonify(errno=RET.THIRDERR, errmsg="发送失败")


# GET /api/v1.0/sms_codes/<mobile>?image_code=xxx&image_code_id=xxx
@api.route("/sms_codes/<re(r'1[345789]\d{9}'):mobile>")
def get_sms_code(mobile):
    """获取短信验证码"""
    # 获取参数
    image_code = request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")

    # 校验参数
    if not all([image_code, image_code_id]):
        # 表示参数不完整
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 业务逻辑处理
    # 从redis中取出真是图片验证码
    try:
        # 有值则返回，无值则返回None
        real_image_code = redis_store.get("image_code_%s" % image_code_id)
    except Exception as e:
        # current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="redis数据库异常")

    # 删除图片验证码，防止用户使用同一个图片验证多次
    try:
        redis_store.delete("image_code_%s" % image_code_id)
    except Exception as e:
        # current_app.logger.error(e)
        pass

    # 判断图片验证码是否过期
    if real_image_code is None:
        # 图片验证码已过期
        return jsonify(errno=RET.NODATA, errmsg="图片验证码已过期")

    # 与用户填写的值进行对比
    if real_image_code.lower() != image_code.lower():
        # 用户填写错误
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")

    # 判断对于这个手机号的操作在60秒内有没有之前的记录，如果有，则认为操作频发，不予处理
    try:
        send_flag = redis_store.get("sms_code_%s" % mobile)
    except Exception as e:
        # current_app.logger.error(e)
        pass
    else:
        if send_flag is not None:
            # 表示在60秒内有过之前的记录
            return jsonify(errno=RET.REQERR, errmsg="请求过于频繁，请60秒后再试")

    # 判断手机号是否存在
    # 有则为对象，无则返回None
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        # current_app.logger.error(e)
        pass
    else:
        if user is not None:
            # 手机号已存在
            return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

    # 如果手机号不存在，则生成短信验证码
    sms_code = "%06d" % random.randint(0, 999999)

    # 保存真实的短信验证码
    try:
        redis_store.setex("sms_code_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 保存发送给这个手机号的记录，防止用户在60秒内再次出现发送短信的操作
        redis_store.setex("send_sms_code_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
    except Exception as e:
        # current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="redis数据库异常")

    # 发送短信
    # try:
    #     ccp = CCP()
    #     result = ccp.send_template_sms(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES/60)], 1)
    # except Exception as e:
    #     # current_app.logger.error(e)
    #     return jsonify(errno=RET.THIRDERR, errmsg="发送异常")
    #
    # if result == 0:
    #     # 表示发送成功
    #     return jsonify(errno=RET.OK, errmsg="发送成功")
    # else:
    #     # 发送不成功
    #     return jsonify(errno=RET.THIRDERR, errmsg="发送失败")

    # 使用celery异步发送短信, delay函数调用后，立即返回
    send_sms.delay(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES/60)], 1)

    # 发送成功，返回值
    return jsonify(errno=RET.OK, errmsg="ok")
