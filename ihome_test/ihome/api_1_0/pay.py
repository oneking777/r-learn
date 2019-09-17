#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys, os
from . import api
from ihome import constants, db
from alipay import AliPay
from flask import current_app, g, jsonify, request
from ihome.models import Order
from ihome.utils.commons import login_required
from ihome.utils.response_code import RET


@api.route("/orders/<int:order_id>/payment", methods=["POST"])
@login_required
def order_pay(order_id):
    """发起支付宝支付"""
    user_id = g.user_id

    # 判断订单状态
    try:
        order = Order.query.filter(Order.id == order_id, Order.user_id == user_id, Order.status == "WAIT_PAYMENT").first()
    except Exception as e:
        # current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    if order is None:
        return jsonify(errno=RET.NODATA, errmsg="数据库异常")

    # 创建支付宝sdk的工具对象
    alipay_client = AliPay(
        appid="2016101000651833",
        app_notify_url=None,
        app_private_key_path=os.path.join(os.path.dirname(__file__), "keys/app_private_key.pem"),
        alipay_public_key_path=os.path.join(os.path.dirname(__file__), "keys/ali_pay_public_key.pem"),
        sign_type="RSA2",
        debug=True
    )

    # 手机网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do + order_string
    order_string = alipay_client.api_alipay_trade_wap_pay(
        out_trade_no=order.id,  # 订单编号
        total_amount=str(order.amount/100.0),  # 总金额
        subject=u"爱家租房 %s " % order.id,  # 订单标题
        return_url="http:127.0.0.1:5000/payComplete.html",  # 回转链接
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    # 构建用户跳转的支付宝链接地址
    pay_url = constants.ALIPAY_URL_PREFIX + order_string
    return jsonify(errno=RET.OK, errmsg="ok", data={"pay_url": pay_url})


@api.route("/order/payment", methods=["PUT"])
def save_order_payment_result():
    """获取支付结果"""
    alipay_dict = request.form.to_dict()

    # 对支付宝参数进行分离操作
    # 提取出sign参数，进行比对
    alipay_sign = alipay_dict.pop("sign")

    # 创建支付宝sdk的工具对象
    alipay_client = AliPay(
        appid="2016101000651833",
        app_notify_url=None,
        app_private_key_path=os.path.join(os.path.dirname(__file__), "keys/app_private_key.pem"),
        alipay_public_key_path=os.path.join(os.path.dirname(__file__), "keys/ali_pay_public_key.pem"),
        sign_type="RSA2",
        debug=True
    )

    # 借助工具验证参数的合法性
    # 如果确定参数是支付宝的，返回True，否则返回false
    result = alipay_client.verify(alipay_dict, alipay_sign)

    if result:
        # 修改数据库的订单状态信息
        order_id = alipay_dict.get("out_trade_no")
        trade_no = alipay_dict.get("trade_no")  # 支付宝的交易号

        try:
            Order.query.filter_by(id=order_id).update({"status": "WAIT_COMMENT", "trade_no": trade_no})
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # current_app.logger.error(e)
    return jsonify(errno=RET.OK, errmsg="ok")