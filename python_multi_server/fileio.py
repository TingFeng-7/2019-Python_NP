import os
os.chdir(r'C:\Users\wtf\Desktop\python网络编程')
with open ('清单.txt','r') as f:
	while True:
		data=f.readline()
		if not data:
			break
		print(data)