#----------------------------------------OOP
#三特征：封装、继承、多态


#----------------------------------------类和实例
#类是实例的模板，实例是具体的对象
class Student(object):
	"""docstring for ClassName"""
	def __init__(self, arg):          #创建实例本身是定义一个特殊的__init__方法，第一参数self必须有，可以把各种属性绑定到self中
		self.arg = arg
name = Student(1)
print(name.arg)	

class Student(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score
bart = Student('Bart Simpson', 59)
print(bart.name)

#数据封装，get_name()、set_name()
#和静态语言不同，Python允许对实例变量绑定任何数据，也就是说，对于两个实例变量，虽然它们都是同一个类的不同实例，但拥有的变量名称都可能不同



#----------------------------------------访问权限
#_name视为私有的可访问变量
#当__name变成_student__name时，就可以被访问



#----------------------------------------继承和多态
#继承
class Animal(object):           #Animal继承了Object对象
	"""docstring for Animal"""
	def __init__(self, arg):
		super(Animal, self).__init__()
		self.arg = arg
		
#多态：在复制（继承）父类的基础之上调用父类方法
#对父类：可复制，不可修改。树

#静态语言vs动态语言
#静态语言说一不二，数据类型必须一致
#动态语言随意而为，只要会跑（有run（））的就是动物
#python属于动态语言



#----------------------------------------获取对象信息
#获取对象类型：type（）
print('123的数据类型：',type(123))
#判断对象类型
print(isinstance(123,int))
#获取一个对象的所有属性和方法

#在len()函数内部，它自动去调用该对象的__len__()方法，所以，下面的代码是等价的：
print(len('ABC'))
print('ABC'.__len__())



#----------------------------------------实力属性和对象属性
class Teacher(object):
	name = 'Tom'

#创建实例
t = Teacher()
print(t.name)
print(Teacher.name)

t.name = 'Jack'
#由于实例的优先级比类属性高，因此，屏蔽掉类的name属性
print(t.name)
#但类的属性并未消失
print(Teacher.name)

#删掉实例name的属性，那么仍然为Tom
del t.name
print(t.name)

Teacher.name = 'Jack'
print(t.name)
print(Teacher.name)


