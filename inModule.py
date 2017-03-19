#-------------------------------------------------常用的第三方模块
#-------------------------------------------------datetime
#获取当前时间
from datetime import datetime
now = datetime.now()
print(now)
#获取指定时间和地点
d = datetime(2015,4,19,12,20)
print(d)
##-------------------------------------------------datetime与timestamp
#时间戳：timestamp = 0 = 1970-1-1 00:00:00 UTC+0:00。。。对应的北京时间：timestamp = 0 = 1970-1-1 08:00:00 UTC+8:00
#全球的时间戳一样，这就是计算机用timestrap的原因

#datetime转化成timestamp
print(d.timestamp())			#timestamp是浮点数，若有小数，小数位表示毫秒数

#某些编程语言（如Java和JavaScript）的timestamp使用整数表示毫秒数，这种情况下只需要把timestamp除以1000就得到Python的浮点表示方法。

#timestamp转化成datetime(有时区的本地时间)
t = 1429417200.0
print(datetime.fromtimestamp(t))
#转为UTC时间
print(datetime.utcfromtimestamp(t))


##-------------------------------------------------datetime与str
#str转换成datetime
cday = datetime.strptime('2015-6-1 18:19:59','%Y-%m-%d %H:%M:%S')
print(cday)

#datetime转换成str
now = datetime.now()
print(now.strftime('%a,%b,%d %H:%M'))

##-------------------------------------------------datetime加减
#需要导入timedelta这个类
from datetime import timedelta
print(now)
print(now + timedelta(hours = 10))
print(now - timedelta(days=1))
print(now + timedelta(days=2, hours=12))
##-------------------------------------------------本地时间转换成UTC时间
#不能强制转换时区
#也不能查询时区
from datetime import timezone
tz_utc_8 = timezone(timedelta(hours = 8))
dt = now.replace(tzinfo = tz_utc_8)
print(dt)
##-------------------------------------------------时区转换(utcnow())
#拿到utc时间，并强制设置成市区为UTC+0：00
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
print(utc_dt)
#astimezone（）将时区转换为北京时间
bj_dt = utc_dt.astimezone(timezone(timedelta(hours = 8)))
print(bj_dt)
#转换成东京时间
tokyo_dt = utc_dt.astimezone(timezone(timedelta(hours = 9)))
print(tokyo_dt)
#将北京时间转换成东京时间
tokyo_dt = bj_dt.astimezone(timezone(timedelta(hours = 8)))
print(tokyo_dt)


#-------------------------------------------------collections
##-------------------------------------------------namedtuple
#为了让tuple的p = （1,2）的二维列表表现的更明显
#又不想定义class，就用namedtuple
from collections import namedtuple
Point = namedtuple('Point',['x','y'])
p = Point(1,2)
print(p.x)
print(p.y)

#namedtuple定义了一个数据类型，是自定义额tuple对象，可定义tuple元素个数，用引用属性而非索引的方式引用tuple的某个元素

# namedtuple('名称', [属性list]):
Circle = namedtuple('Circle', ['x', 'y', 'r'])


##-------------------------------------------------deque
#使用list存储数据时，按索引访问元素很快，但是插入和删除元素就很慢了，因为list是线性存储，数据量大的时候，插入和删除效率很低。
#deque是为了高效实现插入和删除操作的双向列表，适合用于队列和栈：
from collections import deque
d = deque(['a','b','c'])
#增加
d.append('y')
print(d)
#删除
d.pop()		#而非d.pop('a')
print(d)
#首部增加
d.appendleft('x')
print(d)
#首部减少
d.popleft()		#d.popleft('x')
print(d)


##-------------------------------------------------defaultdict
#使用dict时，如果引用的Key不存在，就会抛出KeyError。如果希望key不存在时，返回一个默认值，就可以用defaultdict
from collections import defaultdict
dd = defaultdict(lambda:'N/A')
dd['key1'] = 'abc'
print(dd['key1'])
print(dd['key2'])
#除了在Key不存在时返回默认值，defaultdict的其他行为跟dict是完全一样的

##-------------------------------------------------orderedDict
#dict的key是无序的，但可以用orderedDict使其保持有序，使其按照插入顺序排序
#OrderedDict可以实现一个FIFO（先进先出）的dict，当容量超出限制时，先删除最早添加的Key：
from collections import OrderedDict

class LastUpdatedOrderedDict(OrderedDict):

    def __init__(self, capacity):
        super(LastUpdatedOrderedDict, self).__init__()
        self._capacity = capacity

    def __setitem__(self, key, value):
        containsKey = 1 if key in self else 0
        if len(self) - containsKey >= self._capacity:
            last = self.popitem(last=False)
            print('remove:', last)
        if containsKey:
            del self[key]
            print('set:', (key, value))
        else:
            print('add:', (key, value))
        OrderedDict.__setitem__(self, key, value)



##-------------------------------------------------counter
#简单计数器，用来统计
from collections import Counter 
c = Counter()
for ch in 'python':
	c[ch] = c[ch]+1
print(c)


#-------------------------------------------------base64
#Base64不可用来加密
#Base64就是用64个字符表示任意二进制数据的方法
#Base64的原理：
#		首先，准备一个包含64个字符的数组:['A', 'B', 'C', ... 'a', 'b', 'c', ... '0', '1', ... '+', '/']
#		然后，对二进制数据进行处理，每3个字节一组，一共是3x8=24bit，划为4组，每组正好6个bit
# 		这样我们就可以得到4个数字作为索引->查表->获得相应的4个字符,就是编码后的字符串

#如果要编码的二进制数据不是3的倍数，最后会剩下1个或2个字节怎么办？Base64用\x00字节在末尾补足后，再在编码的末尾加上1个或2个=号，表示补了多少字节，解码的时候，会自动去掉
import base64
print(base64.b64encode(b'binary\x00string'))
print(base64.b64decode(b'YmluYXJ5AHN0cmluZw=='))

#由于标准的Base64编码后可能出现字符+和/，在URL中就不能直接作为参数，所以又有一种"url safe"的base64编码，其实就是把字符+和/分别变成-和_
print(base64.b64encode(b'i\xb7\x1d\xfb\xef\xff'))
print(base64.urlsafe_b64encode(b'i\xb7\x1d\xfb\xef\xff'))
print(base64.urlsafe_b64decode('abcd--__'))

#Base64是一种通过查表的编码方法，不能用于加密，即使使用自定义的编码表也不行。
#Base64适用于小段内容的编码，比如数字证书签名、Cookie的内容等。
#由于=字符也可能出现在Base64编码中，但=用在URL、Cookie里面会造成歧义，所以，很多Base64编码后会把=去掉：
# 标准Base64:
#'abcd' -> 'YWJjZA=='
# 自动去掉=:
#'abcd' -> 'YWJjZA'
#去掉=后怎么解码呢？因为Base64是把3个字节变为4个字节，所以，Base64编码的长度永远是4的倍数，因此，需要加上=把Base64字符串的长度变为4的倍数，就可以正常解码了。

#Base64是一种任意二进制到文本字符串的编码方法，常用于在URL、Cookie、网页中传输少量二进制数据。



#-------------------------------------------------struct
#struct模块解决bytes和其他类型的转换
import struct
print(struct.pack('>I',10240099))	#pack的第一个参数是处理指令，'>I'的意思是：
#>表示字节顺序是big-endian，也就是网络序，I表示4字节无符号整数。H表示两字节无符号整数

#关于bmp文件
s = b'\x42\x4d\x38\x8c\x0a\x00\x00\x00\x00\x00\x36\x00\x00\x00\x28\x00\x00\x00\x80\x02\x00\x00\x68\x01\x00\x00\x01\x00\x18\x00'
print(struct.unpack('<ccIIIIIIHH',s))		#BMP格式采用小端方式存储数据
#关于bmp输出的参数的解释（文件头的结构按顺序如下）
#	两个字节：'BM'表示Windows位图，'BA'表示OS/2位图；
#	一个4字节整数：表示位图大小；
#	一个4字节整数：保留位，始终为0；
#	一个4字节整数：实际图像的偏移量；
#	一个4字节整数：Header的字节数；
#	一个4字节整数：图像宽度；
#	一个4字节整数：图像高度；
#	一个2字节整数：始终为1；
#	一个2字节整数：颜色数。



#-------------------------------------------------hashlib（摘要）
#单向计算特性决定摘要不能加密，只能防篡改
#hashlib提供常见的摘要算法：如MD5，SHA1
#摘要算法也称作哈希算法、散列算法。他通过一个函数，把任意长度的数据转换为长度固定费数据串
import hashlib

md5 = hashlib.md5()
md5.update('how to use python'.encode('utf-8'))
print(md5.hexdigest())

sha1 = hashlib.sha1() 		#SHA1算法，而不是SHAL
sha1.update('how to use python'.encode('utf-8'))
print(sha1.hexdigest())

#摘要算法运用：用户设置的密码就是以摘要算法的方式存入数据库，登录时用明文的摘要与其对比，一样即可成功登陆

#黑客一般不是拿到MD5反推客户的明文密码，而是根据常用的口令得到一个反推表
#为避免被反推，我们可以‘加盐’：通过原始口令加一个复杂的字符串实现
def calc_md5(password):
	return get_md5(password + 'the-Salt')

#相同密码时，如果假定用户无法修改登录名，就可以通过把登录名作为Salt的一部分来计算MD5，从而实现相同口令的用户也存储不同的MD5



#-------------------------------------------------itertools
#itertools模块提供的全部是处理迭代功能的函数，它们的返回值不是list，而是Iterator，只有用for循环迭代的时候才真正计算。
#玩玩无限迭代器先
#无限迭代1：
import itertools
#natuals = itertools.count(1)
#for n in natuals:
#	print(n)			#ctrl+c可以救命


#无限迭代2：
#cs = itertools.cycle('ABC')
#for c in cs:
#	print(c)

#有限迭代3：
ns = itertools.repeat('a',3)		#3代表循环3次
for n in ns:
	print(n)

#takewhile()等函数根据条件判断来截取出一个有限的序列：
natuals = itertools.count(1)
ns = itertools.takewhile(lambda x:x<=10,natuals)
print(list(ns))


##-------------------------------------------------chain
#作用：把迭代对象连接起来
for c in itertools.chain('ABC','EFG'):
	print(c)


##-------------------------------------------------groupby
#作用：把迭代器中相邻重复元素挑出来放在一起
for key,group in itertools.groupby('AAAaBBBBsDDD'):
	print(key,list(group))

#-------------------------------------------------contextlib
#with的用法：with open('/path/to/file', 'r') as f:f.read()
#with的出现是为了避免try。。finall关文件的繁琐

#并不是只有open()函数返回的fp对象才能使用with语句。实际上，任何对象，只要正确实现了上下文管理，就可以用于with语句。

#实现上下文管理是通过__enter__和__exit__这两个方法实现的。例如，下面的class实现了这两个方法：
class Query(object):

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print('Begin')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print('Error')
        else:
            print('End')

    def query(self):
        print('Query info about %s...' % self.name)

#这样我们就可以把自己写的资源对象用于with语句：

with Query('Bob') as q:
    q.query()

##-------------------------------------------------@contextManager
from contextlib import contextmanager

class Query(object):

	def __init__(self,name):
		self.name = name

	def query(self):
		print('Query info about %s...' %self.name)

@contextmanager
def create_query(name):
	print('Begin')
	q = Query(name)
	yield q
	print('End')

with create_query('Bob') as q:
	q.query()
#@contextmanager这个decorator接受一个generator，用yield语句把with ... as var把变量输出出去，然后，with语句就可以正常地工作了

#很多时候，我们希望在某段代码执行前后自动执行特定代码，也可以用@contextmanager实现。例如
@contextmanager
def tag(name):
	print("<%s>" %name)
	yield
	print("<%s>" %name)

with tag("h1"):
	print("Hello")

#@contextmanager让我们通过编写generator来简化上下文管理



##-------------------------------------------------closing
#对象有上下文才可以使用with
#当对象没有上下文时，我们可以使用closing（）来将对象变为上下文
#用with语句使用urlopen（）

from contextlib import closing
from urllib.request import urlopen

with closing(urlopen('https://www.python.org')) as page:
	for line in page:
		print(line)

@contextmanager
def closing(thing):
	try:
		yield thing
	finally:
		thing.close()



#-------------------------------------------------XML
#XML比Json复杂，所以用得比较少
#操作XML有DOM（树）和SAX（流模式）
#理解Python使用Xml中的start_element、end_element、char_data
from xml.parsers.expat import ParserCreate

class DefaultSaxHandler(object):
    def start_element(self, name, attrs):
        print('sax:start_element: %s, attrs: %s' % (name, str(attrs)))

    def end_element(self, name):
        print('sax:end_element: %s' % name)

    def char_data(self, text):
        print('sax:char_data: %s' % text)

xml = r'''<?xml version="1.0"?>
<ol>
    <li><a href="/python">Python</a></li>
    <li><a href="/ruby">Ruby</a></li>
</ol>
'''

handler = DefaultSaxHandler()
parser = ParserCreate()
parser.StartElementHandler = handler.start_element
parser.EndElementHandler = handler.end_element
parser.CharacterDataHandler = handler.char_data
parser.Parse(xml)



#-------------------------------------------------HTMLParser
#要编写一个搜索引擎，第一步用爬虫将目标网站的页面抓下来
#第二步解析该HTML页面，看里面是图片、新闻、还是视频
#虽然Html是xml的子集，但是没有xml语法严格，不能用Xml或者sax解析
#但python提供的HTMLParser就可以很方便的解析Html

from html.parser import HTMLParser
from html.entities import name2codepoint

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print('<%s>' % tag)

    def handle_endtag(self, tag):
        print('</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        print('<%s/>' % tag)

    def handle_data(self, data):
        print(data.replace(u'\xa0', u' '))		#print（data）会报错：'gbk' codec can't decode character

    def handle_comment(self, data):
        print('<!--', data, '-->')

    def handle_entityref(self, name):
        print('&%s;' % name)

    def handle_charref(self, name):
        print('&#%s;' % name)


parser = MyHTMLParser()
parser.feed('''<html>
<head></head>
<body>
<!-- test html parser -->
    <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
</body></html>''')



#-------------------------------------------------urllib
##-------------------------------------------------get
#urllib模块可以非常方便的抓取URL内容，也就是发送一个Get请求到指定的页面，然后返回HTTP的响应

#如果我们要想模拟浏览器发送GET请求，就需要使用Request对象，通过往Request对象添加HTTP头，我们就可以把请求伪装成浏览器。例如，模拟iPhone 6去请求豆瓣首页

from urllib import request

req = request.Request('http://www.douban.com/')
req.add_header('User-Agent','Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')

with request.urlopen(req) as f:
	data = f.read()
	print('Status:',f.status,f.reason)
	for k,v in f.getheaders():
		print('%s:%s' %(k,v))
	print('Data:',f.read().decode('utf-8'))


##-------------------------------------------------post
#要以post发送请求，只需要把参数data一bytes形式传入
#我们模拟一个微博登录，先读取登录的邮箱和口令，然后按照weibo.cn的登录页的格式以username=xxx&password=xxx的编码传入

from urllib import request, parse

print('Login to weibo.cn...')
email = input('Email: ')
passwd = input('Password: ')
login_data = parse.urlencode([
    ('username', email),
    ('password', passwd),
    ('entry', 'mweibo'),
    ('client_id', ''),
    ('savestate', '1'),
    ('ec', ''),
    ('pagerefer', 'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F')
])

req = request.Request('https://passport.weibo.cn/sso/login')
req.add_header('Origin', 'https://passport.weibo.cn')
req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
req.add_header('Referer', 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F')

with request.urlopen(req, data=login_data.encode('utf-8')) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print('Data:', f.read().decode('utf-8'))

##-----------------------------------------------------Handle
#如果还需要更复杂的控制，比如通过一个Proxy去访问网站，我们需要利用ProxyHandler来处理
#示例代码
proxy_handler = urllib.request.ProxyHandler({'http': 'http://www.example.com:3128/'})
proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
proxy_auth_handler.add_password('realm', 'host', 'username', 'password')
opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
with opener.open('http://www.example.com/login.html') as f:
    pass




