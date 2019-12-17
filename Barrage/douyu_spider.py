# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-12-06 14:52


import asyncore
import sys
from queue import Queue
from threading import Thread
import time

DATA_PACKET_TYPE_SEND = 689  # 发送: 客户端发送到服务器
DATA_PACKET_TYPE_RECV = 690  # 接受: 服务器发送到客户端


def encode_content(content):
    """序列化函数"""
    # 需要序列化的数据
    if isinstance(content, str):
        return content.replace(r'@', r'@A').replace(r'/', r'@S')
    elif isinstance(content, dict):
        return r'/'.join(["{}@={}".format(encode_content(k),encode_content(v)) for k,v in content.items()]) + r'/'
    elif isinstance(content, list):
        return r'/'.join([encode_content(data) for data in content]) + r'/'
    else:
        return None

def decode_to_str(content):
    """反序列化函数 - 字符串"""
    # 反序列化字符串数据
    if isinstance(content, str):
        return content.replace(r'@S', r'/').replace(r'@A', r'@')
    else:
        return ""

def decode_to_dict(content):
    """反序列化函数 - 字典"""
    # 反序列化字典数据
    result_dict = dict()
    if isinstance(content, str):
        item_strings = content.split(r'/')
        for item_string in item_strings:
            k_v_list = item_string.split(r'@=')
            if k_v_list is not None and len(k_v_list) > 1:
                k = k_v_list[0]
                v = k_v_list[1]
                result_dict[decode_to_str(k)] = decode_to_str(v)

    return result_dict

def decode_to_list(content):
    """反序列化函数 - 列表"""
    # 反序列化列表数据
    result_list = []
    if isinstance(content, str):
        for item in content.split(r'/')[:-1]:
            result_list.append(decode_to_str(item))
    return result_list


# 定义数据包类
class DataPacket():

    def __init__(self, type=DATA_PACKET_TYPE_SEND, content="", data_bytes=None):
        if data_bytes is None:
            # 数据包的类型(发送与接受)
            self.type = type
            # 数据部分内容
            self.content = content
            self.encrypt_flag = 0
            self.preserve_flag = 0
        else:
            self.type = int.from_bytes(data_bytes[4:6], byteorder="little", signed=False)
            self.encrypt_flag = int.from_bytes(data_bytes[6:7], byteorder="little", signed=False)
            self.preserve_flag = int.from_bytes(data_bytes[7:8], byteorder="little", signed=False)
            # 构建数据部分
            self.content = str(data_bytes[8:-1], encoding="utf-8")

    def get_length(self):
        """获取当前数据包的长度,为以后需要发送数据做准备"""

        # return 4 + 2 + 1 + 1 + len(self.content.encode("utf-8"))
        return 4 + 2 + 1 + 1 + len(self.content.encode("utf-8")) + 1  # \0

    def get_bytes(self):
        """获取二进制的数据"""
        data = bytes()

        # 构建4个字节的消息长度数据
        data_packet_length = self.get_length()

        # to_bytes() 把一个整型数据转换为二进制数据
        # 第一个参数 表示需要转换的二进制数据占几个字节
        # 第二个参数 表示描述字节序
        # 第二个参数 表示设置是否有符号
        data += data_packet_length.to_bytes(4, byteorder="little", signed=False)  # 处理消息长度
        data += self.type.to_bytes(2, byteorder="little", signed=False)  # 处理消息类型
        data += self.encrypt_flag.to_bytes(1, byteorder="little", signed=False)  # 处理消息加密字段
        data += self.preserve_flag.to_bytes(1, byteorder="little", signed=False)  # 处理消息保留字段
        data += self.content.encode("utf-8")  # 处理数据内容

        # 添加 \0 数据
        # 注: 因为在末尾加上\0,所以数据包的长度需要加1
        data += b'\0'

        return data


# 定义Socket客户端类
class DouyuClient(asyncore.dispatcher):


    def __init__(self, host, port, callback=None):
        # 构建发送数据包的队列容器
        # 存放了发送数据包对象
        self.send_queue = Queue()

        # 构建接受数据包的队列容器
        # 存放了接受数据包对象
        self.recv_queue = Queue()

        # 定义外部传入的自定义回调函数
        self.callback = callback

        # 调用父类的初始化方法
        asyncore.dispatcher.__init__(self)
        # super(DouyuClient, self).__init__()

        # 创建Scoket对象
        self.create_socket()
        # 连接服务器
        self.connect((host, port))

        # 构建 专门处理 接受数据包的队列容器中 的数据包的 线程
        self.callback_thread = Thread(target=self.do_callback)
        self.callback_thread.setDaemon(True)  # 守护线程
        self.callback_thread.start()  # 启动线程

        # 构建 心跳 线程
        self.heart_thread = Thread(target=self.do_ping)
        self.heart_thread.setDaemon(True)  # 守护线程
        self.ping_runing = False


    def handle_connect(self):
        print("服务器连接成功...")
        self.start_ping()

    def writable(self):

        # 查看数据包队列容器是否有数据
        # 当返回True时,调用 handle_write 函数
        return self.send_queue.qsize() > 0

    def handle_write(self):

        # 从发送数据包的队列容器中获取数据包对象
        dp = self.send_queue.get()

        # 获取数据包长度,并且发送给服务器
        dp_length = dp.get_length()
        dp_length_data = dp_length.to_bytes(4, byteorder="little", signed=False)
        self.send(dp_length_data)

        # 发送数据包二进制数据到服务器
        self.send(dp.get_bytes())

        self.send_queue.task_done()
        pass

    def readable(self):

        return True

    def handle_read(self):

        # 读取长度,读取的是二进制数据
        data_length_binary = self.recv(4)

        # 通过二进制数据获取length的具体长度
        data_length = int.from_bytes(data_length_binary, byteorder="little", signed=False)

        # 通过数据包的长度获取数据
        data = self.recv(data_length)

        # 通过二进制数据构建数据包对象
        dp = DataPacket(data_bytes=data)

        # 把数据包对象存放到接受数据包的队列容器中
        self.recv_queue.put(dp)

        # print(data)

    def handle_error(self):
        t, e, trace = sys.exc_info()
        print(e)
        self.close()

    def handle_close(self):
        self.stop_ping()
        print("服务器连接关闭")
        self.close()

    def login(self, room_id):

        # 构建登陆数据包 room_id房间号
        # content = "type@=loginreq/roomid@={}/".format(room_id)

        # 保存房间号
        self.room_id = room_id

        # 序列化数据
        send_data = {
            "type":"loginreq",
            "roomid": str(room_id)
        }
        content = encode_content(send_data)
        login_dp = DataPacket(DATA_PACKET_TYPE_SEND, content=content)

        # 把数据包添加到发送数据包的队列容器中
        self.send_queue.put(login_dp)
        pass

    def join_room_group(self):
        """加入弹幕分组"""

        send_data = {
            "type": "joingroup",
            "rid": str(self.room_id),
            "gid": "-9999",
        }
        content = encode_content(send_data)

        dp = DataPacket(type=DATA_PACKET_TYPE_SEND, content=content)
        self.send_queue.put(dp)

        pass

    def send_heart_data_packet(self):
        """"""
        send_data = {
            "type": "mrkl",
        }

        content = encode_content(send_data)
        dp = DataPacket(type=DATA_PACKET_TYPE_SEND, content=content)
        self.send_queue.put(dp)

    def start_ping(self):
        """开启心跳"""
        self.ping_runing = True

    def stop_ping(self):
        """停止心跳"""
        self.ping_runing = False

    def do_ping(self):
        """执行心跳"""
        while True:
            if self.ping_runing:
                self.send_heart_data_packet()
                time.sleep(40)

    def do_callback(self):
        """专门处理 接受数据包的队列容器中 的数据包的 线程"""
        while True:  # 线程永不退出
            # 从接受数据包的队列容器中获取数据包
            dp = self.recv_queue.get()
            # print(" ---> 接受数据!")

            # 对数据进行处理
            # print(dp.content)
            if self.callback is not None:
                # print(" ---> 处理数据")
                self.callback(self, dp)
            self.recv_queue.task_done()


# 定义外部传入的自定义回调函数
def data_callback(client, dp):  # dp 表示数据包对象

    # print("data_callback: " + dp.content)

    # 反序列化响应的数据
    response = decode_to_dict(dp.content)
    print(response)

    if response['type'] == 'loginres':
        print("登陆成功...",response)
        # 调用加入分组请求
        client.join_room_group()

    # 弹幕信息内容
    elif response['type'] == 'chatmsg':
        print("{} 发送的弹幕信息: {}".format(response['nn'], response['txt']))



if __name__ == '__main__':

    client = DouyuClient("openbarrage.douyutv.com", 8601, callback=data_callback)
    # 进入房间
    client.login(383204988)
    asyncore.loop(timeout=10)


    # 测试 序列化数据
    # s = "asdf@ghj/kl"
    # d = {
    #     "name": "ab@45",
    #     "age": "15/a"
    # }
    # l = ['@','@@av','@/A','xyz','//o']
    # print(encode_content(s))
    # print(encode_content(d))
    # print(encode_content(l))

    # 测试 反序列化数据
    # print(decode_to_str(encode_content(s)))
    # print(decode_to_dict(encode_content(d)))
    # print(decode_to_list(encode_content(l)))


    pass


