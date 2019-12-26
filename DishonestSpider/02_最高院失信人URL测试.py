# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator

import requests


url = "http://jszx.court.gov.cn/api/front/getPublishInfoPageList"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
}


data = {
    "pageSize": 10,  # 一页多少条数据
    "pageNo": 2,  # 当前页码
}


response = requests.post(url, data=data, headers=headers)


print(response.status_code)
print(response.content.decode())