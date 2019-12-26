# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DishonestspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 失信人信息存储模型类
class DishonestItem(scrapy.Item):

    name = scrapy.Field()               # 失信人名称
    card_num = scrapy.Field()           # 失信人号码
    age = scrapy.Field()                # 失信人年龄,企业年龄都是0
    area = scrapy.Field()               # 区域
    business_entity = scrapy.Field()    # 法人(企业)
    content = scrapy.Field()            # 失信内容
    publish_date = scrapy.Field()       # 公布日期
    pubilsh_unit = scrapy.Field()       # 公布/执行单位
    create_date = scrapy.Field()        # 创建日期
    update_date = scrapy.Field()        # 更新日期


