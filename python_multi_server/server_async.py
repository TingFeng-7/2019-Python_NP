import os,asyncio
import struct,aiofiles
from eprogress import LineProgress

PORT=('127.0.0.1',8888)#监听端口
BUF_SIZE = 65535#一次接受1024bytes
FileSize_struct = struct.Struct('!I')#文件长度帧
Name_struct=struct.Struct('20s')

def unpack(data):
    (filename,)=Name_struct.unpack(data)
    filename=filename.split(b'\x00')[0]
    #print(filename)
    return filename
#封装发送size长度，然后主函数再传送数据
def cap(writer,filename):
    size=str(os.path.getsize(filename))
    mess=FileSize_struct.pack(int(size))
    #print(mess,len(mess))
    writer.write(mess)
    return int(size)

async def handle_request(reader,writer):
    addr=writer.get_extra_info('peername')
    print('\n'+'id: {} 新客户连接了进来'.format(addr[1]))
    progess=LineProgress(title=str(addr)+'sending')
    data=await reader.read(Name_struct.size)#第一次接受请求
    filename=unpack(data)
    os.chdir(r'C:\Users\wtf\Desktop\python网络编程\SeverList')#服务器文件路径
    #进度条
    count=0
    already_send=0
    try:
        async with aiofiles.open(filename, mode='rb') as f:
            total_size=cap(writer,filename)
            while True:
            #读取固定长度
                data=await f.read(BUF_SIZE)
                count+=1
                #如果没有读到数据,退出循环
                if not data:
                    print('读取完毕')
                    f.close()
                    break
                else:
                    writer.write(data)#发送数据
                    await writer.drain()
                    already_send+=BUF_SIZE
                    progess.update(int((already_send*100)/total_size))
    except Exception as err:
        print('err :',err)
    finally:
        writer.write(b'end') 
        print('本次结束')  

if __name__ == '__main__':
    addr=PORT
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_request, *addr)
    server = loop.run_until_complete(coro)
    print('Listening at {}'.format(addr))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()