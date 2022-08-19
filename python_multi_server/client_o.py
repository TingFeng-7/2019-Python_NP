import socket,struct
import sys,os,time
import argparse
from eprogress import CircleProgress,LineProgress

BUF_SIZE = 65535
HOST=('127.0.0.1',8888)#服务器端口
FileSize_struct = struct.Struct('!I')#文件长度帧
Name_struct=struct.Struct('20s')

#客户端启动tcp套接字
def init_client():
     client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
     return client
#关闭套接字和文件描述符
def terminate(client,f):
     f.close()
     client.close()
     
#封装flag标志结构体
def pack(real_name):
     data=Name_struct.pack(real_name)
     return data

def unpack(data):
     (size,)=FileSize_struct.unpack(data)
     return size


#client module 2.实际下载
def download(new_name,real_name):
     #文件路径切换到下载路径,暂时选在桌面
     os.chdir(r'C:\Users\wtf\Desktop')
     client=init_client()#1.创建
     client.connect(HOST)#2.连接
     real_name=real_name.encode('utf-8')
     progress = LineProgress(title='download loading')
     start=time.time()
     pack(real_name)
     f=open(new_name,'wb')#
     recieved_size=0
     #tcp：sendall
     client.sendall(data)
     #读取size大小
     size=client.recv(FileSize_struct.size)
     if size==b'end':
          print('出错退出')
          sys.exit(0)
     file_total_size=unpack(size)

     print('已收到请求文件大小 {} bytes'.format(file_total_size))
     while recieved_size<file_total_size:
          data=client.recv(BUF_SIZE)
          f.write(data)
          recieved_size+=len(data)
          progress.update(int((recieved_size*100)/file_total_size))
     o=client.recv(FileSize_struct.size)
     if o==b'end':
          print('receive end')     
     terminate(client,f)
     end=time.time()
     print('the task spend {} seconds'.format(end-start))

if __name__ == '__main__':
     FileSize_struct = struct.Struct('!I')
     print(FileSize_struct.size)
     choices={'dl':download}#'multi':thread_download,'':download,'test':mess}
     parser=argparse.ArgumentParser(description='Download file from Server ') 
     parser.add_argument('role',choices=choices,help='which role to play')
     parser.add_argument('-n',metavar='rename', type=str, default='go.msi', 
      help='本地保存文件名')
     parser.add_argument('-o',metavar='name', type=str, default='go.msi', 
      help='服务器真实文件名') 
     args=parser.parse_args()
     function=choices[args.role]
     function(args.n,args.o)




