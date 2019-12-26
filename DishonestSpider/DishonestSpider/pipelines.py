# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DishonestspiderPipeline(object):
    def process_item(self, item, spider):
        return item

import pymysql
from datetime import datetime
from DishonestSpider.settings import MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DB
class DishonestPipeline(object):

    def open_spider(self, spider):
        """建立数据库连接,获取操作数据的cursor"""
        self.connection = pymysql.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD,db=MYSQL_DB)
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        """如果数据不存在,则保存数据"""

        # 判断数据是否存在:如果是自然人根据证件号进行判断;如果是企业/组织,根据企业名称和区域进行判断
        # 年龄,自然人年龄大于0,企业年龄等于0
        if item['age'] == 0:  # 是企业
            # 企业根据 企业名称 和 区域 进行判断 数据是否存在
            select_count_sql = "select COUNT(1) from dishonest where name = '{}' AND area = '{}'".format(item['name'], item['area'])

        else:  # 否则就是自然人
            # 如果证件号是18位,那么就倒数第七位到倒数第四位(不包括第四位),三个数字使用****替换掉
            card_num = item['card_num']
            if len(card_num) == 18:
                card_num = card_num[:-7] + "****" + card_num[-4:]
                # 为了保护失信人隐私与数据格式的一致性,把修改后的数据重新赋值
                item["card_num"] = card_num
            # 自然人根据 证件号 进行判断数据是否存在
            select_count_sql = "select COUNT(1) from dishonest where card_num = '{}'".format(item['card_num'])

        # 执行查询语句
        self.cursor.execute(select_count_sql)
        # 获取查询结果
        count = self.cursor.fetchone()[0]

        # 判断查询结果
        if count == 0:
            # 如果没有数据,就插入数据
            keys, values = zip(*dict(item).items())  # 使用字典特性获取对应的键和值
            insert_sql = "insert into dishonest({}) values({})".format(
                ",".join(keys),
                ",".join(["%s"] * len(values))
            )
            # 执行插入sql数据
            self.cursor.execute(insert_sql, values)
            self.connection.commit()

            # args = [item["age"], item["name"], item["business_entity"], item["card_num"], item["area"], item["content"],
            #         item["pubilsh_unit"], item["publish_date"], item["create_date"], item["update_date"]]
            # insert_sql = "insert into dishonest values (0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            # # 执行插入sql数据
            # self.cursor.execute(insert_sql, args=args)
            # self.connection.commit()

            spider.logger.info("插入数据")

        else:
            # 否则就重复了
            spider.logger.info("数据重复")

        return item

    def close_spider(self, spider):
        """关闭数据库连接"""
        self.cursor.close()
        self.connection.close()


