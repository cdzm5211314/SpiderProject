# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator

import requests

# url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信被执行人&pn=20&rn=10&ie=utf-8&oe=utf-8"
url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA&pn=20&rn=10&ie=utf-8&oe=utf-8&format=json&t=1577253957411&cb=jQuery110206399963484587261_1577246742174&_=1577246742181"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Referer": "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E5%A4%B1%E4%BF%A1%E4%BA%BA&oq=%25E5%25A4%25B1%25E4%25BF%25A1%25E4%25BA%25BA%25E5%2590%258D%25E5%258D%2595&rsv_pq=8d5dd9e100055599&rsv_t=3eedLRsyEfa2bpp%2BZquIs4RfrilbR6haTJ%2BgnIRLrpV8IP%2BBHS9w4vDpdB8&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_sug3=3&rsv_sug1=2&rsv_sug7=100&rsv_sug2=0&inputT=404&rsv_sug4=986&rsv_sug=1"
}


response = requests.get(url, headers=headers)
print(response.status_code)
print(response.content.decode())

