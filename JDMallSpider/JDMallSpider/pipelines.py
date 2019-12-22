# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from JDMallSpider.spiders.jd_category import JdCategorySpider
from JDMallSpider.spiders.jd_product import JdProductSpider
from JDMallSpider.spiders.jd_productredis import JdProductRedisSpider
from JDMallSpider.settings import MONGODB_URL
from scrapy.exceptions import DropItem


class JdmallspiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 商品类别的管道类
class CategoryPipeline(object):

    def open_spider(self, spider):
        """ 当爬虫启动的时候执行 """

        # if spider.name == "jd_category":
        if isinstance(spider, JdCategorySpider):
            # 如果商品类别爬虫就使用此pipeline
            # 开启mongodb连接
            self.client = pymongo.MongoClient(MONGODB_URL)
            self.collection = self.client['jingdong']['jd_category']

            # 添加数据之前先清空集合文档数据
            # self.client.jingdong.jd_category.delete_many({})
            self.collection.delete_many({})

    def process_item(self, item, spider):

        # if spider.name == "jd_category":
        if isinstance(spider, JdCategorySpider):
            # 插入商品类别数据,字典类型数据
            # self.client.jingdong.jd_category.insert_one(dict(item))
            self.collection.insert_one(dict(item))

        # self.collection.insert_one(dict(item))

        # raise DropItem()
        return item  # 如果开启其他pipeline管道,也可以接受此item信息

    def close_spider(self, spider):
        """ 当爬虫关闭的时候执行 """
        # if spider.name == "jd_category":
        if isinstance(spider, JdCategorySpider):
            # 关闭mongodb连接
            self.client.close()
        pass


# 商品信息的管道类
class ProductPipeline(object):

    def open_spider(self, spider):

        # if spider.name == "jd_product":
        if isinstance(spider, JdProductSpider):
            # 如果商品类别爬虫就使用此pipeline
            # 开启mongodb连接
            self.client = pymongo.MongoClient(MONGODB_URL)
            self.collection = self.client['jingdong']['jd_product']

            # 添加数据之前先清空集合文档数据
            # self.client.jingdong.jd_product.delete_many({})
            self.collection.delete_many({})

    def process_item(self, item, spider):

        # if spider.name == "jd_product":
        if isinstance(spider, JdProductSpider):
            # 插入商品信息数据
            # self.client.jingdong.jd_product.insert_one(dict(item))
            self.collection.insert_one(dict(item))

        # raise DropItem()
        return item  # 如果开启其他pipeline管道,也可以接受此item信息

    def close_spider(self, spider):
        # if spider.name == "jd_product":
        if isinstance(spider, JdProductSpider):
            关闭mongodb连接
            self.client.close()
        pass


# 商品信息的管道类 - 分布式
class ProductRedisPipeline(object):

    def open_spider(self, spider):

        # if spider.name == "jd_productredis":
        if isinstance(spider, JdProductRedisSpider):
            # 如果商品类别爬虫就使用此pipeline
            # 开启mongodb连接
            self.client = pymongo.MongoClient(MONGODB_URL)
            self.collection = self.client['jingdong']['jd_product_redis']

            # 添加数据之前先清空集合文档数据
            # self.client.jingdong.jd_product.delete_many({})
            self.collection.delete_many({})

    def process_item(self, item, spider):

        # if spider.name == "jd_productredis":
        if isinstance(spider, JdProductRedisSpider):
            # 插入商品信息数据
            # self.client.jingdong.jd_product.insert_one(dict(item))
            self.collection.insert_one(dict(item))

        # raise DropItem()
        return item  # 如果开启其他pipeline管道,也可以接受此item信息

    def close_spider(self, spider):
        # if spider.name == "jd_productredis":
        if isinstance(spider, JdProductRedisSpider):
            关闭mongodb连接
            self.client.close()


