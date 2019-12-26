# -*- coding: utf-8 -*-

# Scrapy settings for DishonestSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'DishonestSpider'

SPIDER_MODULES = ['DishonestSpider.spiders']
NEWSPIDER_MODULE = 'DishonestSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'DishonestSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# 默认请求头信息
DEFAULT_REQUEST_HEADERS = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Language': 'en',
    # "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    # "Referer": "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E5%A4%B1%E4%BF%A1%E4%BA%BA&oq=%25E5%25A4%25B1%25E4%25BF%25A1%25E4%25BA%25BA%25E5%2590%258D%25E5%258D%2595&rsv_pq=8d5dd9e100055599&rsv_t=3eedLRsyEfa2bpp%2BZquIs4RfrilbR6haTJ%2BgnIRLrpV8IP%2BBHS9w4vDpdB8&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_sug3=3&rsv_sug1=2&rsv_sug7=100&rsv_sug2=0&inputT=404&rsv_sug4=986&rsv_sug=1",
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'DishonestSpider.middlewares.DishonestspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'DishonestSpider.middlewares.DishonestspiderDownloaderMiddleware': 543,
   'DishonestSpider.middlewares.UserAgentDownloaderMiddleware': 343,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'DishonestSpider.pipelines.DishonestspiderPipeline': 300,
   'DishonestSpider.pipelines.DishonestPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# MySQL数据库信息
# 创建数据库: create database dishonest charset='utf8';
# 创建数据库表:
# CREATE TABLE `dishonest` (
#   `dishonest_id` int(11) NOT NULL AUTO_INCREMENT,
#   `age` int(11) NOT NULL COMMENT '年龄,自然人年龄大于0,企业年龄等于0',
#   `name` varchar(255) NOT NULL COMMENT '失信人名称',
#   `business_entity` varchar(255) DEFAULT NULL COMMENT '失信企业法人',
#   `card_num` varchar(255) DEFAULT NULL COMMENT '失信人号码',
#   `area` varchar(255) NOT NULL COMMENT '失信区域',
#   `content` varchar(2000) NOT NULL COMMENT '失信内容',
#   `pubilsh_unit` varchar(255) DEFAULT NULL COMMENT '执行单位',
#   `pubilsh_date` varchar(255) DEFAULT NULL COMMENT '执行时间',
#   `create_date` datetime DEFAULT NULL COMMENT '创建日期',
#   `update_date` datetime DEFAULT NULL COMMENT '更新日期',
#   PRIMARY KEY (`dishonest_id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DB = "dishonest"

