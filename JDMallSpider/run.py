# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator


from scrapy.cmdline import execute

# execute("scrapy crawl spidername".split())
# execute("scrapy crawl spidername --nolog".split())
# execute(["scrapy", "crawl", "spidername"])
# execute(["scrapy", "crawl", "spidername", "--nolog"])

# 运行爬虫
# execute(["scrapy", "crawl", "jd_category"])
# execute(["scrapy", "crawl", "jd_product"])
execute(["scrapy", "crawl", "jd_productredis"])



# 使用os.system函数将字符串转化成命令的方式执行多个爬虫: 顺序执行
# import os
# os.system("scrapy crawl jd_category")
# os.system("scrapy crawl jd_product")



### 使用核心API的方式执行多个爬虫: scrapy.crawler.CrawlerProces
# 该类将为您启动Twisted reactor,配置日志记录并设置关闭处理程序,此类是所有Scrapy命令使用的类
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from scrapy.utils.log import configure_logging
# from JDMallSpider.spiders.jd_category import JdCategorySpider
# from JDMallSpider.spiders.jd_product import JdProductSpider
# configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
# process = CrawlerProcess(settings=get_project_settings())  # 获取settings.py配置文件信息
# process.crawl(JdCategorySpider)
# process.crawl(JdProductSpider)
# process.crawl(*[JdCategorySpider,JdProductSpider])
# process.start()



### 使用核心API的方式执行多个爬虫: scrapy.crawler.CrawlerRunner
# 此类封装了一些简单的帮助程序来运行多个爬虫程序,但它不会以任何方式启动或干扰现有的爬虫
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.project import get_project_settings
# from twisted.internet import reactor
# from scrapy.utils.log import configure_logging
# from JDMallSpider.spiders.jd_category import JdCategorySpider
# from JDMallSpider.spiders.jd_product import JdProductSpider
# configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
# runner = CrawlerRunner(settings=get_project_settings())
# runner.crawl(JdCategorySpider)
# runner.crawl(JdProductSpider)
# d = runner.join()
# d.addBoth(lambda _: reactor.stop())
# reactor.run()

## 或者通过异步执行多个爬虫: 顺序执行
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.project import get_project_settings
# from twisted.internet import reactor, defer
# from scrapy.utils.log import configure_logging
# from JDMallSpider.spiders.jd_category import JdCategorySpider
# from JDMallSpider.spiders.jd_product import JdProductSpider
# configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
# runner = CrawlerRunner(settings=get_project_settings())
# @defer.inlineCallbacks
# def crawl():
#     yield runner.crawl(JdCategorySpider)
#     yield runner.crawl(JdProductSpider)
#     reactor.stop()
# crawl()
# reactor.run()



### 使用自定义Scrapy命令的方式执行多个爬虫:
# 1.在spiders同级目录下新建commands包目录,并在该包目录下新建crawlall.py文件
# 如: 项目名称.项目名称.commands.crawlall.py
# 2.复制Scrapy框架源代码里的commands文件夹的crawl.py源码到新建的crawlall.py文件中
# 如: scrapy.commands.crawl.py
# 3.只修改crawlall.py中的run()方法: 如下所示
# def run(self, args, opts):
#     # 获取项目下的所有爬虫名称列表
#     spider_loader_list = self.crawler_process.spider_loader.list()
#     print(spider_loader_list)
#     # 遍历爬虫名称列表
#     for spidername in spider_loader_list or args:
#         print('此时启动的爬虫名字为: ' + spidername)
#         self.crawler_process.crawl(spidername, **opts.spargs)
#     self.crawler_process.start()
# 4.在settings.py文件配置信息
# COMMANDS_MODULE = '项目名称.新建目录名称'
# 如: COMMANDS_MODULE = 'JDMallSpider.commands'
# 5.启动爬虫使用crawlall命令即可:
# 5.1 可以创建一个文件执行: scrapy.cmdline.execute(["scrapy", "crawlall"])
# 5.2 可以直接在命令行执行: scrapy crawlall --nolog
# execute(["scrapy", "crawlall", "--nolog"])


