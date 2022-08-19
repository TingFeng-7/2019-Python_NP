import socket
import struct
import os

def unpack(data):
    (filename,)=struct.unpack('20s',data)
    filename=filename.split(b'\x00')[0]
    print(filename)
    return filename

def cap(writer,filename):
    size=str(os.path.getsize(filename))
    mess=struct.pack('!I',int(size))
    writer.write(mess)
    return int(size)
