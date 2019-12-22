# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdmallspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 商品类别的存储模型类
class CategoryItem(scrapy.Item):

    b_category_name = scrapy.Field()    # 大分类名称
    b_category_url = scrapy.Field()     # 大分类URL
    m_category_name = scrapy.Field()    # 中分类名称
    m_category_url = scrapy.Field()     # 中分类URL
    s_category_name = scrapy.Field()    # 小分类名称
    s_category_url = scrapy.Field()     # 小分类URL


# 商品信息的存储模型类
class ProductItem(scrapy.Item):

    product_category = scrapy.Field()   # 商品类别
    product_category_id = scrapy.Field()   # 商品类别ID
    product_sku_id = scrapy.Field()     # 商品ID
    product_name = scrapy.Field()       # 商品名称
    product_image_url = scrapy.Field()  # 商品图片URL
    product_book_info = scrapy.Field()  # 图书信息,作者,出版社
    product_option = scrapy.Field()     # 商品选项
    product_shop = scrapy.Field()       # 商品店铺
    product_comments = scrapy.Field()   # 商品评论数量
    product_ad = scrapy.Field()         # 商品促销
    product_price = scrapy.Field()      # 商品价格


