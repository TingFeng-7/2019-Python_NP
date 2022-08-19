import socket
import struct
import os,threading
from eprogress import LineProgress

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

def handle_request(sc,addr):
    print('\n'+'新客户 {} 连接了进来'.format(addr))
    data=sc.recv(Name_struct.size)#第一次接受请求
    name=unpack(data)
    os.chdir(r'C:\Users\wtf\Desktop\python网络编程\SeverList')#服务器文件路径
    progress=LineProgress(title=str(addr)+'sending')
    already_send=0
    try:
        f=open(name,'rb')
        total_size=cap(sc,name)
        while True:
            data=f.read(BUF_SIZE)
            #如果没有读到数据,退出循环
            if not data:
                break
            else:
                sc.sendall(data)
                already_send+=BUF_SIZE
                progress.update(int((already_send*100)/total_size))
        f.close()
    except Exception as err:
        print('err:',err)
    finally:    
        sc.sendall(b'end') 
        print('本次结束')  

while True:
    print('server waiting..')
    sc,addr=server.accept()
    #放入套接字进行处理,这里是处理分割
    try:
        t1 = threading.Thread(target=handle_request, args=(sc,addr))
    # 设置线程守护
        t1.setDaemon(True)
    # 启动线程
        t1.start()
    except Exception as err:
        print('catch error :',err)

