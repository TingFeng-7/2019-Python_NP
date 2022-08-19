#!/usr/bin/env python3
#-*- encoding:utf8 -*-

import socket,struct
from argparse import ArgumentParser

header_struct = struct.Struct('!I')#4字节的size

def recvall(sock,length):
    blocks = []
    while length:
        block = sock.recv(length)
        if not block:
            raise EOFError('socket closed with %d bytes left''in this block'.format(length))
        length -= len(block)
        blocks.append(block)
    return b''.join(blocks)

def get_block(sock):
    data = recvall(sock,header_struct.size)#recvall，4字节size，就是个长度单位
    (blcok_length,) = header_struct.unpack(data)#解压得到长度
    return recvall(sock , blcok_length)#返回一个迭代的函数(sc,再加上算出的长度)


def put_block(sock,message):
    block_length = len(message)
    sock.send(header_struct.pack(block_length))#先打包长度发送
    #在发送message
    sock.send(message)

def server(addr):
    sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1 )
    sock.bind(addr)
    sock.listen(1)
    print('Run this script in another window with "-c" to connect ')
    print('Listening at', sock.getsockname())
    sc,sockname = sock.accept()
    print('Accept connection from ' , sockname)
    sc.shutdown(socket.SHUT_WR)

    while True:
        block = get_block(sc)#
        if not block:break
        print('Block says:' , repr(block))
    sc.close()
    sock.close()

def client(addr):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(addr)
    sock.shutdown(socket.SHUT_RD)
    put_block(sock,b'Beautiful is better than ugly')
    put_block(sock,b'Explicit is better than implicit')
    put_block(sock,b'Simple is better than complex')
    sock.close()

if __name__ == "__main__":
    parser = ArgumentParser(description="Transmit & receive blocks over TCP")
    parser.add_argument('hostname',nargs='?',default='127.0.0.1',
                        help='IP address or Hostname(default:%(default)s)')
    parser.add_argument('-c', action='store_true' , help='run as the client')
    parser.add_argument('-p',type=int,metavar='port',default=1060,
                        help='TCP port number(default:%(default)s)')
    args = parser.parse_args()
    function =client if args.c else server
    function((args.hostname,args.p))