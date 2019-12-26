# -*- coding: utf-8 -*-
import scrapy
import json
from jsonpath import jsonpath
from DishonestSpider.items import DishonestItem
from datetime import datetime

class BaidudishonestSpider(scrapy.Spider):
    name = 'baidudishonest'
    allowed_domains = ['baidu.com']
    start_urls = ['https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信被执行人&pn=20&rn=10&ie=utf-8&oe=utf-8']
    # start_urls = ['https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信被执行人&pn=20&rn=10&ie=utf-8&oe=utf-8&format=json&t=1577253957411']


    def parse(self, response):

        # print(response.text)

        # 响应的Json字符串数据转换为字典数据
        result = json.loads(response.text)

        # 获取总数据条数: dispNum
        disp_num = jsonpath(result, '$..dispNum')[0]
        # print(disp_num)


        # 构建每页请求url,每隔10条数据发送一次请求
        url_pattern = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信被执行人&pn={}&rn=10&ie=utf-8&oe=utf-8"

        for pn in range(0, disp_num, 10):
            url = url_pattern.format(pn)
            yield scrapy.Request(url, callback=self.parse_info)


    def parse_info(self, response):

        # 响应的Json字符串数据转换为字典数据
        datas = json.loads(response.text)
        # print(data)

        # 获取失信人信息列表
        results = jsonpath(datas, '$..result')[0]
        # results = datas['data'][0]['result']
        # print(results)

        # 遍历列表信息,获取具体的信息
        for result in results:
            # print(result)

            item = DishonestItem()

            # 失信人年龄,企业年龄都是0
            item['age'] = int(result['age'])
            # 失信人名称
            item['name'] = result['iname']
            # 法人(企业)
            item['business_entity'] = result['businessEntity']
            # 失信人号码
            item['card_num'] = result['cardNum']
            # 区域
            item['area'] = result['areaName']
            # 失信内容
            item['content'] = result['duty']
            # 公布/执行单位
            item['pubilsh_unit'] = result['courtName']
            # 公布日期
            item['publish_date'] = result['publishDate']
            # 创建日期
            item['create_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 更新日期
            item['update_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 把数据交给引擎
            yield item








