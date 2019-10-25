#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from . import api
from datetime import datetime
from ihome import db, constants, redis_store
from ihome.models import Area, House, Facility, HouseImage, User, Order
from ihome.utils.response_code import RET
from flask import g, current_app, jsonify, request, session
from ihome.utils.commons import login_required
from ihome.utils.image_storage import storage


@api.route("/areas", methods=["GET"])
def get_area_info():
    """获取城区信息"""
    # 尝试从redis中读取数据
    try:
        resp_json = redis_store.get("area_info")
    except Exception as e:
        current_app.logging.error(e)
        pass
    else:
        if resp_json is not None:
            # redis中有缓存数据
            # print("+hit+"*50)
            return resp_json, 200, {"Content-Type": "application/json"}

    # 查询数据库，读取城区信息
    try:
        area_list = Area.query.all()
    except Exception as e:
        # current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据库错误")

    area_dict_li = list()
    # 将对象转换为字典
    for area in area_list:
        area_dict_li.append(area.to_dict())

    # 将数据转换为json字符串
    resp_dict = dict(errno=RET.OK, errmsg="ok", data=area_dict_li)
    resp_json = json.dumps(resp_dict)

    # 缓存机制将数据保存到redis中
    try:
        redis_store.setex("area_info", constants.AREA_INFO_REDIS_CACHE_EXPIRES, resp_json)
    except Exception as e:
        # current_app.logging.error(e)
        pass

    return resp_json, 200, {"Content-Type": "application/json"}


@api.route("/houses/info", methods=["POST"])
@login_required
def save_house_info():
    """保存房屋的基本信息
    前端发送过来的json数据
    {
        "title":"",
        "price":"",
        "area_id":"1",
        "address":"",
        "room_count":"",
        "acreage":"",
        "unit":"",
        "capacity":"",
        "beds":"",
        "deposit":"",
        "min_days":"",
        "max_days":"",
        "facility":["7","8"]
    }
    """

    # 提取数据
    user_id = g.user_id
    house_data = request.get_json()
    # print("++"*50)
    # print(house_data)

    title = house_data.get("title")  # 房屋名称标题
    price = house_data.get("price")  # 房屋单价
    area_id = house_data.get("area_id")  # 房屋所属城区的编号
    address = house_data.get("address")  # 房屋地址
    room_count = house_data.get("room_count")  # 房屋包含的房间数目
    acreage = house_data.get("acreage")  # 房屋面积
    unit = house_data.get("unit")  # 房屋布局（几室几厅)
    capacity = house_data.get("capacity")  # 房屋容纳人数
    beds = house_data.get("beds")  # 房屋卧床数目
    deposit = house_data.get("deposit")  # 押金
    min_days = house_data.get("min_days")  # 最小入住天数
    max_days = house_data.get("max_days")  # 最大入住天数

    # 校验参数
    if not all(
            [title, price, area_id, address, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(RET.PARAMERR, errmsg="参数不完整")

    # 校验金额
    try:
        price = int(float(price) * 100)
        deposit = int(float(deposit) * 100)
    except Exception as e:
        # current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 判断城区id是否存在
    try:
        area = Area.query.get(area_id)
    except Exception as e:
        # current_app.logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    if area is None:
        return jsonify(errno=RET.NODATA, errmsg="城区信息有误")

    print("-------it is ok  1---------")

    # 保存房屋信息
    house = House(
        user_id=user_id,
        area_id=area_id,
        title=title,
        price=price,
        address=address,
        room_count=room_count,
        acreage=acreage,
        unit=unit,
        capacity=capacity,
        beds=beds,
        deposit=deposit,
        min_days=min_days,
        max_days=max_days
    )
    # try:
    #     db.session.add(house)
    #     # db.commit()
    # except Exception as e:
    #     # db.session.rollback()
    #     # current_app.logging.error(e)
    #     return jsonify(RET.DBERR, errmsg="保存数据异常")

    print("-------it is ok   2---------")

    # 处理房屋配置信息
    facility_ids = house_data.get("facility")
    # print(facility_ids)

    # 如果用户勾选了设施信息，再保存数据库
    if facility_ids:
        # ["7", "8"]
        try:
            facilities = Facility.query.filter(Facility.id.in_(facility_ids)).all()
        except Exception as e:
            # current_app.logging.error(e)
            return jsonify(errno=RET.DBERR, errmsg="数据库异常")

        if facilities:
            # 表示有合法的设施数据
            # 保存设施数据
            house.facilities = facilities

    print("-------it is ok   3---------")

    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        # current_app.logging.error(e)
        db.session.rollback()
        return jsonify(RET.DBERR, errmsg="保存数据异常")

    print("-------it is ok    4---------")

    return jsonify(errno=RET.OK, errmsg="ok", data={"house_id": house.id})


@api.route("/houses/image", methods=["POST"])
@login_required
def save_house_image():
    """保存房屋图片
    :param 图片， 房屋id
    """
    image_file = request.files.get("house_image")
    house_id = request.form.get("house_id")

    if not all([image_file, house_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 判断house_id 的正确性
    try:
        house = House.query.get(house_id)
    except Exception as e:
        # current_app.logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    if house is None:
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    # 保存图片到七牛
    image_data = image_file.read()
    try:
        file_name = storage(image_data)
    except Exception as e:
        # current_app.logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    # 保存图片名字到数据库
    house_image = HouseImage(house_id=house_id, url=file_name)
    db.session.add(house_image)

    # 处理房屋的主图片
    if not house.index_image_url:
        house.index_image_url = file_name
        db.session.add(house)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # current_app.logging.error(e)
        return jsonify(RET.DBERR, errmsg="保存图片异常")

    image_url = constants.QINIU_URL_DOMAIN + file_name

    return jsonify(errno=RET.OK, errmsg="ok", data={"image_url": image_url})


@api.route("/user/houses", methods=["GET"])
@login_required
def get_user_houses():
    """获取用户发布的房源"""
    # 获取用户的id
    user_id = g.user_id

    # 查询数据库
    try:
        user = User.query.get(user_id)
        houses = user.houses
    except Exception as e:
        # current_app.logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取数据失败")

    # 将查询的房屋信息转换为字典存放到列表中
    houses_list = list()
    if houses:
        for house in houses:
            houses_list.append(house.to_basic_dict())
    return jsonify(errno=RET.OK, errmsg="OK", data={"houses": houses_list})


@api.route("/houses/index", methods=["GET"])
def get_house_index():
    """获取房屋列表页面"""
    # 尝试从缓存中读取数据
    try:
        ret = redis_store.get("home_page_data")
    except Exception as e:
        # current_app.logger.error(e)
        ret = None

    if ret:
        print("hit house index page redis")
        # 缓存中有数据, 直接返回
        return '{"errno": 0, "errmsg": "ok", "data": %s}' % ret, 200, {"Content-Type": "application/json"}
    else:
        # 查询数据库，返回房屋订单数目最多的5条数据
        try:
            houses = House.query.order_by(House.order_count.desc()).limit(constants.HOME_PAGE_MAX_HOUSES)
        except Exception as e:
            # current_app.logging.error(e)
            return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

        if not houses:
            return jsonify(errno=RET.NODATA, errmsg="查询无数据")

        houses_list = list()
        for house in houses:
            # 如果房屋没有设置主图片，则跳过
            if not house.index_image_url:
                continue
            houses_list.append(house.to_basic_dict())

        # 将数据转换为json，并保存到redis缓存
        json_houses = json.dumps(houses_list)  # "[{}, {}, {}]"
        try:
            redis_store.setex("home_page_data", constants.HOME_PAGE_DATA_REDIS_EXPIRES, json_houses)
        except Exception as e:
            # current_app.logging.error(e)
            pass

        return '{"errno": 0, "errmsg": "ok", "data": %s}' % json_houses, 200, {"Content-Type": "application/json"}


@api.route("/houses/<int:house_id>", methods=["GET"])
def get_house_detail(house_id):
    """获取房屋详情页面"""
    # 前端在房屋详情页面展示时，如果浏览页面的用户不是该房屋的房东，则展示预定按钮，否则不展示，
    # 所以需要后端返回登录用户的user_id
    # 尝试获取用户登录的信息，若登录，则返回给前端登录用户的user_id，否则返回user_id=-1

    user_id = session.get("user_id", "-1")

    # 校验参数
    if not house_id:
        return jsonify(errno=RET.PARAMERR, errmsg="参数缺失")

    # 先尝试从缓存中获取信息
    try:
        ret = redis_store.get("house_info_%s" % house_id)
    except Exception as e:
        # current_app.logger.error(e)
        ret = None
    if ret:
        print("hit house detail page redis")
        return '{"errno":"0", "errmsg":"OK", "data":{"user_id":%s, "house":%s}}' % (user_id, ret), \
               200, {"Content-Type": "application/json"}

    # 查询数据库
    try:
        house = House.query.get(house_id)
    except Exception as e:
        # current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

    if not house:
        return jsonify(errno=RET.NODATA, errmsg="房屋不存在")

    print("----------it is ok 1-----------")

    # 将房屋对象数据转换为字典
    try:
        house_data = house.to_full_dict()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="数据出错")

    print("--------it is ok 2----------")

    # 存入到redis中去
    json_house = json.dumps(house_data)
    try:
        redis_store.setex("house_info_%s" % house_id, constants.HOUSE_DETAIL_REDIS_EXPIRE_SECOND, json_house)
    except Exception as e:
        # current_app.logger.error(e)
        pass
    resp = '{"errno":"0", "errmsg":"OK", "data":{"user_id":%s, "house":%s}}' % (user_id, json_house), \
           200, {"Content-Type": "application/json"}
    return resp


# GET  api/v1.0/houses?sd=2019-07-21&ed=2019-07-22&aid=17&sk=new&p=1
@api.route("/houses", methods=["GET"])
def get_house_list():
    """获取房屋的列表信息（搜索页面）"""
    start_data = request.args.get("sd", "")  # 用户想要的起始时间
    end_data = request.args.get("ed", "")  # 用户想要的结束时间
    area_id = request.args.get("aid", "")  # 地区编号
    sort_key = request.args.get("sk", "")  # 排序关键字
    page = request.args.get("p")  # 页数

    # 处理时间
    try:
        if start_data:
            start_data = datetime.strptime(start_data, "%Y-%m-%d")

        if end_data:
            end_data = datetime.strptime(end_data, "%Y-%m-%d")

        if start_data and end_data:
            assert start_data <= end_data
    except Exception as e:
        # current_app.logging.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 判断区域id
    if area_id:
        try:
            area = Area.query.get(area_id)
        except Exception as e:
            # current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 处理页数
    try:
        page = int(page)
    except Exception as e:
        # current_app.logger.error(e)
        page = 1

    # 使用缓存
    redis_key = "house_%s_%s_%s_%s" % (start_data, end_data, area_id, sort_key)

    try:
        resp_json = redis_store.hget(redis_key, page)
    except  Exception as e:
        # current_app.logger.error(e)
        pass
    else:
        if resp_json:
            print("hit house list page redis")
            return resp_json, 200, {"Content-Type": "application/json"}

    # 过滤条件的参数容器
    filter_params = list()

    # 填充过滤参数
    # 时间条件
    conflict_orders = None
    try:
        if start_data and end_data:
            # 查询冲突的订单
            conflict_orders = Order.query.filter(Order.begin_date <= end_data, Order.end_date >= start_data).all()

        elif start_data:
            conflict_orders = Order.query.filter(Order.end_date >= start_data).all()

        elif end_data:
            conflict_orders = Order.query.filter(Order.begin_date <= end_data).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    if conflict_orders:
        # 从订单中获取冲突的房屋id
        conflict_house_ids = [order.house_id for order in conflict_orders]

        # 如果冲突的房屋id不为空，向查询参数中添加条件
        if conflict_house_ids:
            filter_params.append(House.id.notin_(conflict_house_ids))

    # 区域条件
    if area_id:
        filter_params.append(House.area_id == area_id)

    # 查询数据库
    # 补充排序条件
    if sort_key == "booking":
        house_query = House.query.filter(*filter_params).order_by(House.order_count.desc())
    elif sort_key == "price-inc":
        house_query = House.query.filter(*filter_params).order_by(House.price.asc())
    elif sort_key == "price-des":
        house_query = House.query.filter(*filter_params).order_by(House.price.desc())
    else:  # 新旧
        house_query = House.query.filter(*filter_params).order_by(House.create_time.desc())

    # 处理分页
    #                               当前页数        每页数量                                    自动错误输出
    try:
        page_obj = house_query.paginate(page=page, per_page=constants.HOUSE_LIST_PAGE_CAPACITY, error_out=False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 获取页面数据
    house_li = page_obj.items
    houses = list()
    for house in house_li:
        houses.append(house.to_basic_dict())

    # 获取总页数
    total_page = page_obj.pages

    resp_dict = dict(errno=RET.OK, errmsg="ok", data={"total_page": total_page, "houses": houses, "current_page": page})
    resp_json = json.dumps(resp_dict)

    # 设置缓存数据
    if page <= total_page:
        redis_key = "house_%s_%s_%s_%s" % (start_data, end_data, area_id, sort_key)
        # 哈希类型
        try:
            # redis_store.hset(redis_key, page, resp_json)
            # redis_store.expire(redis_key, constants.HOUSE_LIST_PAGE_CACHE_EXPIRES)

            # 创建redis管道对象，可以一次执行多个语句
            pipeline = redis_store.pipeline()
            # 开启多个语句的记录
            pipeline.multi()

            pipeline.hset(redis_key, page, resp_json)
            pipeline.expire(redis_key, constants.HOUSE_LIST_PAGE_CACHE_EXPIRES)

            # 执行语句
            pipeline.execute()

        except Exception as e:
            # current_app.logger.error(e)
            pass

    return resp_json, 200, {"Content-Type": "application/json"}