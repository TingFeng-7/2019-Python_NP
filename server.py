import socket
import struct
import os
BUF_SIZE = 1024#一次接受1024bytes
DOWN_FLAG=0
UP_FLAG=1
GET_FLAG=2

def uploadreq(server,name,size,client_addr):
    count=0
    os.chdir(r'C:\Users\wtf\Desktop\python网络编程\csdn_udp\SeverList')
    name=Fname.split(b"\x00")[0]
    if size>0:
        print ('client ip：',client_addr,' File name is:',name,"字节大小是",size)
        f=open(name,'wb')#写模式打开
        server.sendto(b'ok',client_addr) #发送就绪,接收结构体
        while True:
            data,client_addr=server.recvfrom(BUF_SIZE)
            if data!=b'end': #0-9，接受bytes
                f.write(data)
                print ('received'+str(count)+'次接受自 ',client_addr,'\\n')
                count+=1
            else:
                break
    #正常情况下回复消息
        server.sendto('ok'.encode('utf-8'),client_addr)
        count+=1
        f.close()
        print('循环了'+str(count))
    else:
        print("该文件为空")

server_addr = ('127.0.0.1',8888)
server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind(server_addr)
#循环接受客户端发送数据,并将数据发回
count=0

while True:
    if count==0:
        print ("Are You Ready?")
        data,client_addr = server.recvfrom(BUF_SIZE)
        Fname,size,flag=struct.unpack('20sII',data)
        print('来自',client_addr,'的连接')
        os.chdir(r'C:\Users\wtf\Desktop\python网络编程\csdn_udp\SeverList') #服务器端路径 \是转义符
        if flag==UP_FLAG:
            # uploadreq(server,Fname,size,client_addr)
            # count=0
            name=Fname.split(b"\x00")[0]#因为会用\x00填充
            if size>0:
                print ('client ip：',client_addr,' File name is:',name,"字节大小是",size)
                f=open(name,'wb')#写模式打开
                server.sendto(b'ok',client_addr) #发送就绪,接收结构体
            else:
                print("该文件为空")
            while True:
                data,client_addr=server.recvfrom(BUF_SIZE)
                if data!=b'end': #0-9，接受bytes
                    f.write(data)
                    print ('received'+str(count)+'次接受自 ',client_addr,'\n')
                    count+=1
                else:
                    break
            #回复消息
                server.sendto('ok'.encode('utf-8'),client_addr)
                count+=1
            print('循环了'+str(count))
            f.close()
            count=0 #就再次循环
        elif flag==GET_FLAG:
            a=os.listdir()
            flist=''
            print(a)
            for line in a:
                flist+=str(line)+'%'
                print('\n')
                print(line)
            data=flist.encode('utf-8')
            server.sendto(data,client_addr)
            print('已发送我方列表')
            count=0
        elif flag==DOWN_FLAG:
            #根据名字查找打开文件
            name=Fname.split(b"\x00")[0]
            down_count=1
            f=open(name,'rb')
            while True:
                data=f.read(BUF_SIZE)
                if data!=b'':
                    server.sendto(data,client_addr)
                    print('server already send',down_count)
                    down_count+=1
                else:
                    break
                echo,client_addr=server.recvfrom(BUF_SIZE)
            server.sendto(b'end',client_addr)
            f.close()

#打包文件元祖消息并发送
server.close()
