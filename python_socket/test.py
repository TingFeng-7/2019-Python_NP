import socket
import struct
client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_addr=('127.0.0.1',8880)
#data=b'hello'
name='wtf'
name=name.encode('utf-8')
size=1024
flag=22
data=struct.pack('20sii',name,size,flag)
client.sendto(data,server_addr)
print('waitting')
data,addr=client.recvfrom(1024)
print(data)
client.close()