#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: kang.cunhua@qq.com
# @Date:   2016-06-07 10:10:54
# @Last Modified by:   kang.cunhua@qq.com
# @Last Modified time: 2016-07-03 18:33:38
from flask import current_app
from flask import render_template
from app.base import LazyImport
import requests
import json
from app.models import db, GraphiteKeys, GraphiteGroupKey


def api_action(method="", params=None):
    """Summary

   Args:
        method (str, optional): 调用的(模块.方法)
        params (dict, optional): 参数

    Returns:
        json: 远程调用结果
    """
    if params is None:
        params = {}
    try:
        module, func = method.split(".")
    except ValueError as e:
        current_app.logger.warning("method传值错误: {}".format(e.message))
        return False

    lazyimport = LazyImport(module, func)
    if not lazyimport.isValidModule():
        current_app.logger.warning("{} 模块不可用".format(module))
        return False
    if not lazyimport.isValidMethod():
        current_app.logger.warning("{} 函数不可用".format(func))
        return False

    try:
        called = lazyimport.getCallMethod()
        if callable(called):
            return called(**params)
        else:
            current_app.logger.warning("{}.{} 函数不能被调用".format(module, func))
            return False

    except Exception as e:
        current_app.logger.warning("调用模块执行中出错: {}".format(e.message))
    return False


def api_action_diff_host(method="", params=""):
    """域外调用例子# api 和 web nginx 不在同一个主机，类似测试test_api的调用方法

    Args:
        method (str, optional): 调用的方法名
        params (dict, optional): 参数

    Returns:
        json: 远程调用结果
    """
    url = "http://127.0.0.1:5000/api"
    header = {
        "content-type": "application/json"
    }
    data = {
        "jsonrpc": 2.0,
        "method": method,
        "id": 0,
        "auth": None,
        "params": params
    }
    r = requests.post(url, headers=header, data=json.dumps(data))
    return r


def check_field_exists(obj, data, field_none=[]):
    for field in data.keys():
        if not hasattr(obj, field):
            current_app.logger.warning("参数错误, {} 不在这个{}表里".format(field, obj))
            raise Exception("Params error: {} is not in this table".format(field))
        if not data.get(field, None):
            if not field_none:
                continue
            current_app.logger.warning("参数错误, {} 不能为空".format(field))
            raise Exception("Params error: {} is empty".format(field))


def check_output_field(obj, data):
    if not isinstance(data, list):
        current_app.logger.warning("output 必须是list")
        raise Exception("output 必须是list")
    for field in data:
        if not hasattr(obj, field):
            current_app.logger.warning("{} 输出字段不存在".format(field))
            raise Exception("{} 输出字段不存在".format(field))


def check_order_by(obj, order_by):
    tmp_order_by = order_by.split()
    if len(tmp_order_by) != 2:
        current_app.logger.warning("order by 参数不正确")
        raise Exception("order by 参数不正确")

    order_by_list = ["desc", "asc"]
    if tmp_order_by[1].lower() not in order_by_list:
        current_app.logger.warning("排序参数不正确, 值可以为 {}".format(order_by_list))
        raise Exception("排序参数不正确, 值可以为 {}".format(order_by_list))
    if not hasattr(obj, tmp_order_by[0].lower()):
        current_app.logger.warning("排序字段不在表中")
        raise Exception("排序字段不在表中")
    return tmp_order_by


def check_limit(limit):
    if not str(limit).isdigit():
        current_app.logger.warning("limit 值必须为数字")
        raise Exception("limit 值必须为数字")


def process_result(data, output):
    ret = []
    for obj in data:
        if output:
            tmp = {}
            for j in output:
                tmp[j] = getattr(obj, j)
            ret.append(tmp)
        else:
            tmp = obj.__dict__
            tmp.pop("_sa_instance_state")
            ret.append(tmp)
    return ret


def check_update(obj, data, where):
    if not data:
        current_app.logger.warning("没有要更新数据")
        raise Exception("没有要更新数据")
    for field in data.keys():
        if not hasattr(obj, field):
            current_app.logger.warning("需要更新的 {} 这个字段不存在".format(field))
            raise Exception("需要更新的 {} 这个字段不存在".format(field))
    if not where:
        current_app.logger.warning("需要提供where条件")
        raise Exception("需要提供where条件")
    if not where.get("id", None):
        current_app.logger.warning("需要提供ID作为更新条件")
        raise Exception("需要提供ID作为更新条件")
    if str(where.get("id")).isdigit():
        if int(where.get("id")) <= 0:
            current_app.logger.warning("id的值为大于0的整数")
            raise Exception("id的值为大于0的整数")
        else:
            where = {"id": where.get("id")}
    else:
        current_app.logger.warning("ID必须为数字")
        raise Exception("ID必须为数字")


def jump(ret, success_url="/", error_url="/"):
    success = "public/success.html"
    error = "public/error.html"
    if ret:
        return render_template(success, next_url=success_url)
    else:
        return render_template(error, next_url=error_url)


class Treeview(object):

    def __init__(self):
        self.product_info = api_action("product.get", {"output": ["id", "module_letter", "pid"]})
        self.idc_info = api_action("idc.get", {"output": ["id", "name"]})
        self.data = []

    def get_child_node(self):
        ret = []
        for p in filter(lambda x: True if x.get("pid", None) == 0 else False, self.product_info):
            node = {}
            node['text'] = p.get("module_letter", None)
            node['id'] = p.get("id", None)
            node["type"] = "service"
            node["nodes"] = self.get_grant_node(p.get("id", None))
            ret.append(node)
        return ret

    def get_grant_node(self, pid):
        ret = []
        for p in filter(lambda x: True if x.get("pid", None) == pid else False, self.product_info):
            node = {}
            node['text'] = p.get("module_letter", None)
            node['id'] = p.get("id", None)
            node["type"] = "product"
            node["pid"] = pid
            ret.append(node)
        return ret

    def get(self, idc=False):
        child = self.get_child_node()
        if not idc:
            return child


def get_product():
    products = api_action("product.get", {"output": ["module_letter", "id", "pid"]})
    print products
    bus = [product for product in products if product['pid'] == 0]  # 业务线信息
    data = []
    for b in bus:
        sec_product = get_sec_product(products, b['id'])
        for p in sec_product:
            performance_data = {}
            service_id = b['id']
            server_purpose = p['id']
            performance_data['product'] = "{}/{}".format(b['module_letter'], p['module_letter'])
            performance_data['hostlist'] = get_hostlist_by_group(service_id, server_purpose)
            performance_data['item'] = get_graphite_key_by_group(server_purpose)
            data.append(performance_data)
    return data


def get_graphite_key_by_group(server_purpose):
    graphite_key_ids = db.session.query(GraphiteGroupKey).filter_by(service_id=server_purpose).all()
    key_data = db.session.query(GraphiteKeys).filter(GraphiteKeys.id.in_(
        [graphite.key_id for graphite in graphite_key_ids])).all()
    return [{"key": key.name, "type": key.type, "title": key.title} for key in key_data]


def get_sec_product(products, pid):
    ret = []
    for product in products:
        if product['pid'] == pid:
            ret.append(product)
    return ret


def get_hostlist_by_group(service_id, server_purpose):
    where = {
        "service_id": service_id,
        "server_purpose": server_purpose
    }
    hostlist = api_action("server.get", {"output": ["hostname"], "where": where})
    print hostlist
    return [host['hostname'] for host in hostlist]
