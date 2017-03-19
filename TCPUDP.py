#---------------------------------------------------网络编程
#---------------------------------------------------TCP/IP协议
#互联网协议簇
#ip地址、ip协议、数据包
#TCP是建立在IP上的，握手
#ipv4，ipv6

#---------------------------------------------------TCP
#比如我在浏览器向新浪发送请求，浏览器是客户端，新浪是服务器端
#Socket表示打开一个网络连接
##---------------------------------------------------客户端
import socket
#创建一个socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)	#AF_INET之ID能够使用ipv4协议，AF_INET6指定ipv6
														#SOCK_STREAM指定使用面向流的TCP协议
#建立连接
s.connect(('www.sina.com.cn',80))							#参数是一个tuple，80是WEB服务的标准端口，25是SMTP,21是FTP
#发送数据
s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')

#接收数据
buffer = []
while True:
	#每次最多接收1k字节
	d = s.recv(1024)		#recv(max)
	if d:
		buffer.append(d)
	else:
		break
data = b''.join(buffer)
#关闭连接
s.close()

header,html = data.split(b'\r\n\r\n',1)
print(header.decode('utf-8'))
#把接收的数据写入文件
with open('sina.html','wb') as f:
	f.write(html)

##---------------------------------------------------服务器端
#玩：将客户端发过来的字符循环加上Hello再发回去
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#绑定监听的地址和端口
s.bind(('127.0.0.1',9999))			#tuple
s.listen(5)		#listen(max)
print('Writing for conection...')
while True:
	#接受一个新连接
	sock,addr = s.accept()
	#创建新线程来处理TCP连接
	t = threading.Thread(target=tcplink,args=(sock,addr))
	t.start()

def tcplink(sock,addr):
    print('Accept new connection from %s:%s...' % addr)		#IndentationError: unindent does not match any outer indentation level
    														#复制装逼失败啊
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)

#---------------------------------------------------UDP
#TCP是建立可靠连接，并且通信双方都可以以流的形式发送数据
#UDP是面向无连接的协议
##---------------------------------------------------服务端
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		#socket.SOCK_DGRAM的类型是UDP

# 绑定端口:
s.bind(('127.0.0.1', 9999))

print('Bind UDP on 9999...')
while True:							#不需要listen
    # 接收数据:
    data, addr = s.recvfrom(1024)
    print('Received from %s:%s.' % addr)
    s.sendto(b'Hello, %s!' % data, addr)			#sendto()就可以把数据用UDP发给客户端


##---------------------------------------------------客户端
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for data in [b'Michael', b'Tracy', b'Sarah']:
    # 发送数据:
    s.sendto(data, ('127.0.0.1', 9999))
    # 接收数据:
    print(s.recv(1024).decode('utf-8'))
s.close()









