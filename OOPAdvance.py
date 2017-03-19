#-------------------------------------------面向对象高级编程
#-------------------------------------------使用__slots__
#Java中的单例模式
class Student(object):
	__slots__ = ('name','age')
#所以往里面存储属性时：Student.score，报错AttributeError
#但是，__slots__仅仅对当前实例有效


#-------------------------------------------使用@property
#用set_score、get_score可以限制属性、检查属性，但是调用这两个办法又太麻烦
#于是用到了@property装饰器，把一个方法变成属性调用
class Screen(object):
	@property
	def score(self):
		return self._score

	@score.setter
	def score(self,value):
		self.score = value


#请利用@property给一个Screen对象加上width和height属性，以及一个只读属性resolution：
class Screen(object):
	@property
	def width(self):
		return self.width

	@width.setter
	def width(self,width):
		if not isinstance(width,int):
			raise ValueError('width must be int type')
		self._width = width

	@property
	def height(self):
		return self.height

	@height.setter
	def height(self,height):
		if  not isinstance(height,int):
			raise ValueError('height must be int type')
		self._height = height
	#只读属性，没有setter方法
	@property
	def resolution(self):
		return self._width*self._height

	
s = Screen()
s.width = 1024
s.height = 768
print(s.resolution)


#-------------------------------------------多重继承
#由于Python允许使用多重继承，因此，MixIn就是一种常见的设计。
#只允许单一继承的语言（如Java）不能使用MixIn的设计。



#-------------------------------------------定制类
#__str__()
#__str__()方法，返回一个好看的字符串就可以了
#这是因为直接显示变量调用的不是__str__()，而是__repr__()，两者的区别是__str__()返回用户看到的字符串，而__repr__()返回程序开发者看到的字符串，也就是说，__repr__()是为调试服务的。
class Student(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Student object (name=%s)' % self.name
    __repr__ = __str__
s = Student('Jack')
print('look me',s)
print('mmmmmm')


#__iter__()
#如果一个类想被用于for ... in循环，类似list或tuple那样，就必须实现一个__iter__()方法，该方法返回一个迭代对象，然后，Python的for循环就会不断调用该迭代对象的__next__()方法拿到循环的下一个值，直到遇到StopIteration错误时退出循环。
class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1 # 初始化两个计数器a，b

    def __iter__(self):
        return self # 实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b # 计算下一个值
        if self.a > 100000: # 退出循环的条件
            raise StopIteration();
        return self.a # 返回下一个值
for n in Fib():
	print(n)

#__getitem__()
#要表现得像list那样按照下标取出元素，需要实现__getitem__()方法：
class Fib(object):
    def __getitem__(self, n):
        a, b = 1, 1
        for x in range(n):
            a, b = b, a + b
        return a

f = Fib()     
print(f)   
#__getattr__
#当调用不存在的属性时，比如score，Python解释器会试图调用__getattr__(self, 'score')来尝试获得属性，这样，我们就有机会返回score的值：
class Student(object):

    def __init__(self):
        self.name = 'Michael'

    def __getattr__(self, attr):
        if attr=='score':
            return 99
class Student(object):

    def __init__(self):
        self.name = 'Michael'

    def __getattr__(self, attr):
        if attr=='score':
            return 99
        if attr=='age':
            return lambda: 25
        raise AttributeError('\'Student\' object has no attribute \'%s\'' % attr)

s = Student()
print(s.name)
print(s.score)
print(s.age())
# AttributeError: 'Student' object has no attribute 'grade'
#print(s.grade)

#这实际上可以把一个类的所有属性和方法调用全部动态化处理了，不需要任何特殊手段。
#这种完全动态调用的特性有什么实际作用呢？作用就是，可以针对完全动态的情况作调用。
#举个例子：
#现在很多网站都搞REST API，比如新浪微博、豆瓣啥的，调用API的URL类似：
#http://api.server/user/friends
#http://api.server/user/timeline/list
#如果要写SDK，给每个URL对应的API都写一个方法，那得累死，而且，API一旦改动，SDK也要改。
#利用完全动态的__getattr__，我们可以写出一个链式调用：
class Chain(object):

    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        return Chain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path

    __repr__ = __str__
print(Chain().status.user.timeline.list)
#这样，无论API怎么变，SDK都可以根据URL实现完全动态的调用，而且，不随API的增加而改变！
#还有些REST API会把参数放到URL中，比如GitHub的API：
#GET /users/:user/repos
#调用时，需要把:user替换为实际用户名。如果我们能写出这样的链式调用：
#Chain().users('michael').repos
#就可以非常方便地调用API了。有兴趣的童鞋可以试试写出来。



#-------------------------------------------枚举类（Enum）
from enum import Enum,unique

@unique           #用unique装饰器检查是否重复
class Weekday(Enum):
	Sun = 0
	Mon = 1
	Tue = 2
	Wed = 3
	Thu = 4
	Fri = 5
	Sat = 6

day1 = Weekday.Tue
print(day1.value)
	


#-------------------------------------------使用元类
#type（） 检查类型的方法
#要创建一个class对象，type()函数依次传入3个参数：
#class的名称；
#继承的父类集合，注意Python支持多重继承，如果只有一个父类，别忘了tuple的单元素写法；
#？？？tuple的单元素写法
#class的方法名称与函数绑定，这里我们把函数fn绑定到方法名hello上。

#除了使用type()动态创建类以外，要控制类的创建行为，还可以使用metaclass
#定义metaclass->创建类->创建实例
#高一班主任教我的，快看快看，我变魔术，变变变


' Simple ORM using metaclass '

#首先来定义Field类，它负责保存数据库表的字段名和字段类型：
class Field(object):

    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)

#在Field的基础上，进一步定义各种类型的Field，比如StringField，IntegerField等等：
class StringField(Field):

    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')

class IntegerField(Field):

    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')

#下一步，就是编写最复杂的ModelMetaclass了：
class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        print('Found model: %s' % name)
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                print('Found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
        for k in mappings.keys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = name # 假设表名和类名一致
        return type.__new__(cls, name, bases, attrs)

#以及基类Model：
class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))

# testing code:

class User(Model):
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')

u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')
u.save()