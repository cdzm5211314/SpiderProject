# -*- coding: utf-8 -*-
import scrapy
import json
from DishonestSpider.items import DishonestItem
from datetime import datetime

class CourtdishonestSpider(scrapy.Spider):
    name = 'courtdishonest'
    allowed_domains = ['court.gov.cn']
    # start_urls = ['http://jszx.court.gov.cn/api/front/getPublishInfoPageList']

    post_url = "http://jszx.court.gov.cn/api/front/getPublishInfoPageList"

    # 构建起始请求
    def start_requests(self):
        data = {
            "pageSize": "10",
            "pageNo": "1",
        }

        # 构建post请求,交给引擎
        yield scrapy.FormRequest(self.post_url, formdata=data, callback=self.parse)


    def parse(self, response):

        # print(response.text)

        # 把响应的Json数据转换为字典数据
        results = json.loads(response.text)

        # 解析第一页数据,获取总页数
        page_count = results['pageCount']

        # 构建每一页的请求
        for page_no in range(1, page_count):

            data = {
                "pageSize": "10",
                "pageNo": str(page_no),
            }

            yield scrapy.FormRequest(self.post_url, formdata=data, callback=self.parse_data)


    def parse_data(self, response):

        # print(response.text)

        # 把响应的Json数据转换为字典数据
        results = json.loads(response.text)

        # 获取所需数据
        datas = results['data']

        for data in datas:

            item = DishonestItem()
            # 失信人年龄,企业年龄都是0
            item['age'] = int(data['age'])
            # 失信人名称
            item['name'] = data['name']
            # 法人(企业)
            item['business_entity'] = data['buesinessEntity']
            # 失信人号码
            item['card_num'] = data['cardNum']
            # 区域
            item['area'] = data['areaName']
            # 失信内容
            item['content'] = data['duty']
            # 公布/执行单位
            item['pubilsh_unit'] = data['courtName']
            # 公布日期
            item['publish_date'] = data['publishDate']
            # 创建日期
            item['create_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 更新日期
            item['update_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 把数据交给引擎
            # print(item)
            yield item



