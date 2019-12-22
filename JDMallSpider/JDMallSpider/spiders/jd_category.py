# -*- coding: utf-8 -*-
import scrapy
import json
from JDMallSpider.items import CategoryItem


class JdCategorySpider(scrapy.Spider):
    name = 'jd_category'
    allowed_domains = ['dc.3.cn']
    start_urls = ['https://dc.3.cn/category/get']
    # start_urls = ['https://dc.3.cn/category/get?&callback=getCategoryCallback']

    def parse(self, response):

        # print(response.body.decode('GBK'))
        # 把响应的Json数据转换Python字典类型数据
        result = json.loads(response.body.decode('GBK'))

        # 获取所有的分类数据列表
        datas = result['data']

        # 遍历数据所有分类数据列表,获取所有的大分类数据
        for data in datas:

            # 创建商品类别的模型类对象
            categoryItem = CategoryItem()


            b_category = data['s'][0]  # 获取所有的大分类字典数据
            b_category_info = b_category['n']  # 获取大分类信息
            m_category_list = b_category['s']  # 获取大分类下的所有中分类数据列表
            # print("大分类信息: {}".format(b_category_info))

            # b_category_name, b_category_url = self.get_category_name_url(b_category_info)
            categoryItem['b_category_name'], categoryItem['b_category_url'] = self.get_category_name_url(b_category_info)

            # 遍历中分类数据列表,获取所有中分类信息
            for m_category in m_category_list:
                m_category_info = m_category['n']  # 获取中分类信息
                s_category_list = m_category['s']  # 获取中分类下的所有小分类数据列表
                # print("中分类信息: {}".format(m_category_info))

                m_category_name, m_category_url = self.get_category_name_url(m_category_info)
                categoryItem['m_category_name'], categoryItem['m_category_url'] = self.get_category_name_url(m_category_info)

                # 遍历小分类数据列表,获取所有小分类信息
                for s_category in s_category_list:
                    s_category_info = s_category['n']  # 获取小分类信息
                    # print("小分类信息: {}".format(s_category_info))

                    # s_category_name, s_category_url = self.get_category_name_url(s_category_info)
                    categoryItem['s_category_name'], categoryItem['s_category_url'] = self.get_category_name_url(s_category_info)

                    # print(categoryItem)
                    yield categoryItem


    # 分析小分类信息数据有三种格式,如:
    # 1. 小分类信息: i-list.jd.com/list.html?cat=14065,14137,14138|实验室试剂||0
    # ---> 分析得到这种格式的信息中都包含有'jd.com'
    # 2. 小分类信息: 1713-4758|杂志/期刊||0
    # ---> 进行URL地址拼接:https://channel.jd.com/1713-4758.html
    # 3. 小分类信息: 9855-17084-17089|管材管件||0
    # ---> 进行URL地址拼接: https://list.jd.com/list.html?cat=9987,12854,16941

    def get_category_name_url(self, category_info):
        """ 
        根据大中小分类信息,提取各分类的名称与URL
        :param category_info: 大中小分类信息
        :return: 分类的名称与URl
        """
        category_list = category_info.split('|')  # 根据分类信息进行数据分割,得都一个列表
        # 如: ['12218-13586-13588 ', '鸭肉', '', '0']

        category_url = category_list[0]     # 获取分类URL
        category_name = category_list[1]    # 获取分类名称

        # 根据分类信息数据的三种格式进行分别处理URL
        if category_url.count('jd.com') == 1:
            # 第一种数据格式: i-list.jd.com/list.html?cat=14065,14137,14138
            category_url = 'https://' + category_url
        elif category_url.count('-') == 1:
            # 第二种数据格式: 1713-4758
            # https://channel.jd.com/1713-4758.html
            category_url = 'https://channel.jd.com/{}.html'.format(category_url)
        else:
            # 第三种格数据式: 9855-17084-17089
            # https://list.jd.com/list.html?cat=9987,12854,16941
            category_url = 'https://list.jd.com/list.html?cat={}'.format(category_url.replace('-', ','))

        # 返回分类的名称与URL
        return category_name, category_url


