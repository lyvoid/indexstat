# -*-coding:utf-8-*-
from pymongo import MongoClient
from config.config import config


def init():
    client = MongoClient(config['db_host'], 27017)
    # 创建数据库
    db = client[config['db_name']]
    # 创建Collect
    userinfo = db['szindex']
    # 创建索引
    userinfo.create_index('date', unique=True)
