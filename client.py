import socket,struct
import sys,os
import argparse
BUF_SIZE = 1024
DOWN_FLAG=0
UP_FLAG=1
GET_FLAG=2

#客户端启动
def init_client():
     client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
     server_addr=('127.0.0.1',8888)
     return client,server_addr
#关闭套接字和文件
def terminate(client,f):
     f.close()
     client.close()
     
#封装flag标志结构体
def pack(name,size,flag):
     data=struct.pack('20sII',name,size,flag)
     return data
#client module 1.下载文件，先对路径处理路径
def do_path(data_path,flag):
     name=str(data_path).split('\\')[-1] 
     try:
          size=os.path.getsize(data_path)  #获取文件大小
     except FileNotFoundError:
          print('该文件不存在')
     else:
          name=name.encode('utf-8')  
          data=pack(name,size,flag)
     print(data_path)
     print(size)
     return data

def getlist(data_path):
     client,server_addr=init_client()
     data=pack(b'',0,GET_FLAG)#前两位为0或空
     client.sendto(data,server_addr)
     print('client sent request')
     data,addr=client.recvfrom(BUF_SIZE)#等待信息返回
     print('the server files as fllows:')
     data=data.decode('utf-8')
     filel=data.split('%')
     for line in filel:
          print(line)
#上传请求
def upload(data_path):
     #创建套接字
     client,server_addr=init_client()
     data=do_path(data_path,UP_FLAG)#路径处理
     print(data)
     f=open(data_path,'rb')
     count=0
     while True:
          if count==0:#计数还未开始，只执行一次
               client.sendto(data,server_addr)
               recv_data,addr = client.recvfrom(BUF_SIZE)#等待server 返回就绪
               if recv_data == b'ok':
                    print("客户端准备就绪")
          #循环执行          
          data=f.read(BUF_SIZE)#先读1024字节
          if data != b'':
          #每次按最大字节来读取发送
               client.sendto(data,server_addr)
               count+=1   
               print('client are uploading',str(count)+"times")
          else:#读不出数据了
               client.sendto('end'.encode('utf-8'),server_addr)
               break
          #data, server_addr = client.recvfrom(BUF_SIZE)     
     print('循环了'+str(count)+'次数据')#一共发送了机
     terminate(client,f)

#client module 2.实际下载
def download(name):
     #读取文件名
     os.chdir(r'C:\Users\wtf\Desktop\python网络编程\python_udp\Download')
     client,server_addr=init_client()
     name=name.encode('utf-8')
     print(name)
     data=pack(name,0,DOWN_FLAG)
     f=open(name,'wb')
     print('已准备创建新文件')
     client.sendto(data,server_addr)
     print('已发送请求信息')
     count=0
     while True:
          data,server_addr=client.recvfrom(BUF_SIZE)
          count+=1
          if count==0:
               print('服务器正在向我们发送数据')
          elif data==b'end':
               print('接收完毕')
               break
          print('client are downloading',count,'下载')
          f.write(data)#写数据
          name=b'ok'
          data=pack(name,0,DOWN_FLAG)
          #client.sendto(b'ok',server_addr)#发送OK
     terminate(client,f)

    
def mess(mess):
     client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
     server_addr=('127.0.0.1',8888)
     mess=mess.encode('utf-8')
     client.sendto(mess,server_addr)
     print('已发送信息')
     client.close()


if __name__ == '__main__':
     choices={'upload':upload,'get':getlist,'download':download,'test':mess}
     parser=argparse.ArgumentParser(description='Choose download or get') 
     parser.add_argument('role',choices=choices,help='which role to play')
     parser.add_argument('path',metavar='path', type=str, default='', 
      help='要上传的文件路径')
     args=parser.parse_args()
     function=choices[args.role]
     function(args.path)
     #print(args.path)



