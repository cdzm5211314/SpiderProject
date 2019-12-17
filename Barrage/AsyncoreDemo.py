# -*- coding:utf-8 -*-
# @Desc : 客户端Socket基本开发使用
# @Author : Administrator
# @Date : 2019-12-06 9:45

# Python的asyncore模块提供了以异步的方式写入套接字服务的客户端和服务器的基础结构
# 模块主要包括:
#     asyncore.loop(…): 用于循环监听网络事件。loop()函数负责检测一个字典，字典中保存dispatcher的实例。
#     asyncore.dispatcher类: 一个底层套接字对象的简单封装。这个类有少数由异步循环调用的，用来事件处理的函数。
#         dispatcher类中的writable()和readable()在检测到一个socket可以写入或者数据到达的时候被调用，并返回一个bool值，决定是否调用handle_read或者handle_write。
#     asyncore.dispatcher_with_send类: 一个 dispatcher的子类，添加了简单的缓冲输出能力，对简单的客户端很有用。

import asyncore
import sys


# 1.定义类并继承 asyncore.dispatcher
class SocketClient(asyncore.dispatcher):

    # 2.实现类中的回调函数代码
    # 2.1类的初始化方法
    def __init__(self, host, port):

        # 2.1.1调用父类的方法
        asyncore.dispatcher.__init__(self)

        # 2.1.2创建Socket对象
        self.create_socket()

        # 2.1.3链接服务器
        address = (host, port)
        self.connect(address)

    # 2.2实现 handle_connect 回调函数
    # 当Socket连接服务器成功时回调该函数
    def handle_connect(self):
        print("handle_connect - 与服务器连接成功...")

    # 2.3实现 writable 回调函数
    # 描述是否有数据需要被发送到服务器,返回True表示可写(如果不实现默认返回True),返回False表示不可写;当返回True时触发handle_write函数
    def writable(self):
        print("writable - 是否有数据进行可写或不可写")

        return True

    # 2.4实现 handle_write 回调函数
    # 当有数据需要发送时(writable回调函数返回True时),触发该函数,通常情况在该函数中编写send方法发送数据
    def handle_write(self):
        print("handle_write - 有数据需要写入服务器")
        # 内部实现对服务器发送数据的代码
        self.send("hello world ".encode("utf-8"))  # send发送数据时,参数类型为字节数据

    # 2.5实现 readable 回调函数
    # 描述是否有数据需要从服务器读取,返回True表示有数据需要读取(如果不实现默认返回True),返回False表示无数据需要读取,当返回True时触发handle_read函数
    def readable(self):
        print("readable - 是否有数据进行读取或不读取")

        return True

    # 2.6实现 handle_read 回调函数
    # 当有数据需要读取时(readable回调函数返回True时),触发该函数,通常情况在该函数中编写recv方法接受(读取)数据
    def handle_read(self):
        print("handle_read - 有数据需要从服务器读取")
        # 主动接受数据,参数是需要接受数据的长度
        result = self.recv(1024)
        print(result)

    # 2.7实现 handle_error 回调函数
    # 当程序运行过程中发生异常时回调该函数
    def handle_error(self):
        print("handle_error - 程序运行时发生异常...")
        # 编写处理错误的方法
        # t表示错误的类型,e表示具体错误信息说明,trace表示跟踪错误对象位置
        t, e, trace = sys.exc_info()
        print(e)
        self.close()

    # 2.8实现 handle_close 回调函数
    # 当连接关闭是回调该函数
    def handle_close(self):
        print("handle_close - 与服务器连接关闭...")
        self.close()  # 真正关闭Socket连接


# 3.创建对象并执行 asyncore.loop 进入运行循环
if __name__ == "__main__":
    socketClient = SocketClient("127.0.0.1",9999)
    # 开始启动运行循环
    asyncore.loop(timeout=5)  # timeout 表示一次循环所需要的时长


