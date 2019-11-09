import struct
import os,time
import socketserver
BUF_SIZE = 1024#一次接受1024bytes
DOWN_FLAG=0
UP_FLAG=1
GET_FLAG=2
PORT=8888

def unpack(data):
    name,size,flag=struct.unpack('20sII',data)
    return name,size,flag

#1.服务器该怎么处理请求

class UdpHandller(socketserver.BaseRequestHandler):
    def handle(self):
        count=0
        print('the task initiate at:',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        if count==0:
            data=self.request[0]#取出bytes数据,其实是名字
            Fname,size,flag=unpack(data)#拆分结构体
            print("addr is :",self.client_address)
            os.chdir(r'C:\Users\wtf\Desktop\python网络编程\python_udp\SeverList') #服务器端路径
            #1.处理上传请求
            #Do Upload_Request
            if flag==UP_FLAG:
                name=Fname.split(b'\x00')[0]
                if size>0:
                    print ('client ip：',self.client_address,' File name is:',name,"字节大小是",size)
                    f=open(name,'wb')#写模式打开
                    self.request[1].sendto(b'ok',self.client_address) #发送就绪,准备接受bytes数据
                else:
                    print("该文件为空")
                while True:
                    #NOTICE:这里的client_addr与self.client_address值相同
                    data,client_addr=self.request[1].recvfrom(BUF_SIZE)
                    if data!=b'end': #0-9，接受bytes
                        f.write(data)
                        print (str(count)+'.',client_addr,'客户端',client_addr,'上传文件中')
                        count+=1
                    else:
                        break
                #回复消息
                    self.request[1].sendto('ok'.encode('utf-8'),client_addr)
                    count+=1
                print('循环了'+str(count),'文件',name,'上传完毕')
                f.close()
            #处理获取文件列表
            #2.Do GetList_Request
            elif flag==GET_FLAG:
                a=os.listdir()
                flist=''
                for line in a:
                    flist+=str(line)+'%'
                data=flist.encode('utf-8')
                self.request[1].sendto(data,self.client_address)
                print('已向',self.client_address,'发送我方列表')
            #处理下载请求
            #3.do Download_Request
            elif flag==DOWN_FLAG:
                #根据名字查找打开文件
                name=Fname.split(b"\x00")[0]
                down_count=1
                f=open(name,'rb')
                while True:
                    data=f.read(BUF_SIZE)
                    if data!=b'':
                        self.request[1].sendto(data,self.client_address)
                        print('server are sending',down_count,'to',self.client_address)
                        down_count+=1
                    else:
                        break
                    #data,client_addr=self.request[1].recvfrom(BUF_SIZE)#阻塞返回的ok
                self.request[1].sendto(b'end',self.client_address)
                print('客户端下载结束')
                f.close()

#2选择一个合适的服务类型，mixin和udpsever，决定是多线程处理并发
class ThreadingUdpServer(socketserver.ThreadingMixIn,socketserver.UDPServer):
        daemon_threads=True
        def __init__(self,sever_addr,RequestHandler):
            socketserver.UDPServer.__init__(self,sever_addr,RequestHandler)

server=ThreadingUdpServer(('127.0.0.1',PORT),UdpHandller)
try:
    server.serve_forever()
except KeyboardInterrupt:
    sys.exit(0)     