# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator

from redis import StrictRedis
from pymongo import MongoClient
from JDMallSpider.settings import MONGODB_URL,REDIS_URL
from JDMallSpider.spiders.jd_productredis import JdProductRedisSpider
import pickle


# 把MonogoDB数据的数据转存到Redis数据库
def category_from_mongodb_to_redis():

    # redis数据库连接
    redis_client = StrictRedis.from_url(REDIS_URL)
    # mongodb数据库连接
    mongo_client = MongoClient(MONGODB_URL)

    # 读取MongoDB中的分类信息,序列化字典数据后,添加到商品信息爬虫的redis-key指定的list
    # 获取MongoDB数据库的集合
    collection = mongo_client['jingdong']['jd_category']
    # 读取分类信息
    cursor = collection.find()
    for category in cursor:
        # 序列化字典数据
        data = pickle.dumps(category)
        # 添加到商品信息爬虫的redis-key指定的list
        redis_client.lpush(JdProductRedisSpider.redis_key, data)

    # 关闭MongoDB数据库
    mongo_client.close()


if __name__ == '__main__':

    category_from_mongodb_to_redis()


