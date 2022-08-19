import socket
import struct
import os,threading
from eprogress import LineProgress
import cap

PORT=('127.0.0.1',8888)#监听端口
BUF_SIZE = 65535#一次接受1024bytes
FileSize_struct = struct.Struct('!I')#文件长度帧
Name_struct=struct.Struct('20s')

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(PORT)

#z最大连接数是50
server.listen(50)

def unpack(data):
    (filename,)=Name_struct.unpack(data)
    filename=filename.split(b'\x00')[0]
    print(filename)
    return filename
#封装
def cap(sc,name):
    size=str(os.path.getsize(name))
    mess=FileSize_struct.pack(int(size))
    sc.sendall(mess)
    return int(size)

while True:
    print('server waiting..')
    sc,addr=server.accept()
    print('新客户 {} 连接了进来'.format(addr))
    #放入套接字进行处理
    data=sc.recv(Name_struct.size)
    name=unpack(data)
    progress=LineProgress(title=str(addr)+'sending')
    print(name.decode('utf-8'))
    os.chdir(r'C:\Users\wtf\Desktop\python网络编程\SeverList')#服务器文件路径

    already_send=0
    try:
        f=open(name,'rb')
        total_size=cap(sc,name)
        count=0
        while True:
            data=f.read(BUF_SIZE)
            count+=1
            #如果没有读到数据,退出循环
            if not data:
                break
            else:
                sc.sendall(data)
                already_send+=BUF_SIZE
                progress.update(int((already_send*100)/total_size))
                # print(' {} sending..to client'.format(count))
        f.close()
    except Exception as err:
        print('err:',err)
    finally:    
        sc.sendall(b'end') 
        print('本次结束')  