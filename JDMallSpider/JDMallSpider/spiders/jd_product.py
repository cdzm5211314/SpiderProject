# -*- coding: utf-8 -*-
import scrapy
import json
from jsonpath import jsonpath
from JDMallSpider.items import ProductItem

class JdProductSpider(scrapy.Spider):
    name = 'jd_product'
    allowed_domains = ['jd.com', '3.cn']
    # start_urls = ['http://jd.com/']

    def start_requests(self):
        category = {
            "b_category_name": "家用电器",
            "b_category_url": "https://jiadian.jd.com",
            "m_category_name": "电视",
            "m_category_url": "https://list.jd.com/list.html?cat=737,794,798",
            "s_category_name": "超薄电视",
            "s_category_url": "https://list.jd.com/list.html?cat=737,794,798&ev=4155_76344&sort=sort_rank_asc&trans=1&JL=2_1_0#J_crumbsBar"
        }

        yield scrapy.Request(category['s_category_url'], callback=self.parse, meta={"category":category})


    def parse(self, response):

        # print(response.text)

        # 取出传递过来的数据
        category = response.meta['category']

        # 获取每页商品的SKU_ID
        sku_ids = response.xpath('//div[@id="plist"]/ul/li/div/@data-sku').extract()

        for sku_id in sku_ids:

            # 创建商品信息的模型类对象
            productItem = ProductItem()

            productItem['product_category'] = category  # 商品类别
            productItem['product_sku_id'] = sku_id      # 商品ID

            # 根据每个sku_id拼接商品的详情页url
            url = "https://item.jd.com/{}.html".format(sku_id)

            # 模拟手机端请求访问商品详情页
            url = "https://cdnware.m.jd.com/c1/skuDetail/apple/7.3.0/{}.json".format(sku_id)

            # 构建商品详情页请求
            yield scrapy.Request(url, callback=self.parse_product_info, meta={'productItem':productItem})

        # 获取下一页url
        next_url= response.xpath('//a[@class="pn-next"]/@href').extract_first()

        # 判断是否有下一页
        if next_url is not None:  #  表示有下一页
            # 拼接下一页的url
            # url = 'https://list.jd.com' + next_url
            url = response.urljoin(next_url)
            # print("下一页URL地址信息: ", url)

            # 构建下一页请求
            yield scrapy.Request(url, callback=self.parse, meta={'category':category})


    def parse_product_info(self, response):

        # print("商品详情页URL地址信息: ", response.url)

        # 取出传递过来的数据
        productItem = response.meta['productItem']

        # 把响应的数据转换为字典数据
        result = json.loads(response.text)

        # 提取数据: 商品名称
        productItem['product_name'] = result['wareInfo']['basicInfo']['name']
        # 提取数据: 商品图片URL
        productItem['product_image_url'] = result['wareInfo']['basicInfo']['wareImage'][0]['small']
        # 提取数据: 图书信息,作者,出版社
        productItem['product_book_info'] = result['wareInfo']['basicInfo']['bookInfo']
        # 提取数据: 商品选项
        color_size = jsonpath(result, '$..colorSize')  # 如果有值返回一个列表
        if color_size:
            # 注: colorSize的值本身就是一个列表
            color_size = color_size[0]
            product_option = {}
            for option in color_size:
                title = option['title']
                value = jsonpath(option, '$..text')
                product_option[title] = value
            productItem['product_option'] = product_option
        # 提取数据: 商品店铺
        shop = jsonpath(result, '$..shop')  # 如果有值返回一个列表
        if shop:
            shop = shop[0]
            if shop:  # shop有值的情况
                productItem['product_shop'] = {
                    'shop_id': shop['shopId'],
                    'shop_name': shop['name'],
                }
            else:  # shop没有值的情况
                productItem['product_shop'] = {
                    'shop_name': '京东自营店',
                }
        # 提取数据: 商品类别ID
        productItem['product_category_id'] = result['wareInfo']['basicInfo']['category'].replace(";", ",")

        # print(productItem)

        # 构建商品促销URL
        product_ad_url = 'https://cd.jd.com/promotion/v2?skuId={}&area=5_142_42540_0&venderId=1000004123&cat={}'.format(productItem['product_sku_id'], productItem['product_category_id'])

        # 构建商品促销请求
        yield scrapy.Request(product_ad_url, callback=self.parse_product_ad, meta={'productItem':productItem})


    def parse_product_ad(self, response):

        # 取出传递过来的数据
        productItem = response.meta['productItem']
        # print(productItem)

        # 把响应的数据转换为字典数据
        # print(response.text)
        result = json.loads(response.text)

        # 提取数据: 商品促销
        productItem['product_ad'] = jsonpath(result, '$..ad')[0] if jsonpath(result, '$..ad') else ''
        # ads = jsonpath(result, '$..ads')  # 如果有值返回一个列表
        # if ads:
        #     ads = ads[0]
        #     if ads:  # 表示商品有促销活动
        #         productItem['product_ad'] = ads[0]

        # print(productItem)

        # 构建商品评价URL
        product_comments_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}'.format(productItem['product_sku_id'])

        # 构建商品评价请求
        yield scrapy.Request(product_comments_url, callback=self.parse_product_comments, meta={'productItem': productItem})


    def parse_product_comments(self, response):

        # 取出传递过来的数据
        productItem = response.meta['productItem']
        # print(productItem)

        # 把响应的数据转换为字典数据
        # print(response.text)
        result = json.loads(response.text)

        # 提取数据: 商品评论数量(评价数量,好评数量,差评数量,好评率)
        productItem['product_comments'] = {
            'CommentCount': jsonpath(result, '$..CommentCount')[0],
            'GoodCount': jsonpath(result, '$..GoodCount')[0],
            'PoorCount': jsonpath(result, '$..PoorCount')[0],
            'GoodRate': jsonpath(result, '$..GoodRate')[0],
        }

        # print(productItem)

        # 构建商品价格URL
        product_price_url = 'https://p.3.cn/prices/mgets?skuIds=J_{}'.format(productItem['product_sku_id'])

        # 构建商品价格请求
        yield scrapy.Request(product_price_url, callback=self.parse_product_price, meta={'productItem': productItem})


    def parse_product_price(self, response):

        # 取出传递过来的数据
        productItem = response.meta['productItem']
        # print(productItem)

        # 把响应的数据转换为字典数据
        # print(response.text)
        result = json.loads(response.text)

        # 提取数据: 商品价格
        productItem['product_price'] = result[0]['p']

        # print(productItem)

        yield productItem


