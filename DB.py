#-----------------------------------------------------------访问数据库
#菲关系型数据库：NOSQL
#关系型数据库
#sqlite的占位符是？，mysql的占位符是%s
#由于Python的DB-API定义都是通用的，所以，操作MySQL的数据库代码和SQLite类似。

#-----------------------------------------------------------使用SQLite
#SQLite是一个嵌入式数据库
#要点：conn、cursor
#导入数据库
import sqlite3
#连接sqlite数据库
#数据库文件是test.db,如果文件不存在，会自动在当前目录创建
conn = sqlite3.connect('test.db')
#创建一个cursor
cursor = conn.cursor()
#执行一条sql语句，创建user表
#cursor.execute('create table user (id varchar(20) primary key,name varchar(20))')
#继续执行sql语句，插入一条记录
cursor.execute('insert into user (id, name) values (\'3\', \'Michael\')')
#通过rowcount获取插如的行数
print(cursor.rowcount)
#关闭cursor
cursor.close()
#提交事务
conn.commit()
#关闭connection
conn.close()



conn = sqlite3.connect('test.db')
cursor = conn.cursor()
#执行查询语句
cursor.execute('select * from user where id = ?',('1',))
#获取查询结果
values = cursor.fetchall()
print(values)
cursor.close()
conn.close()

#-----------------------------------------------------------使用Mysql
##-----------------------------------------------------------安装Mysql
#mysql -u roor -p
#root

##-----------------------------------------------------------安装Mysql驱动
#在命令行窗口运行，安装驱动
#pip install mysql-connector-python --allow-external mysql-connector-python
#若失败运行：pip install mysql-connector

#导入Mysql驱动
import mysql.connector

conn = mysql.connector.connect(user='root',password='root',database='test')
cursor = conn.cursor()

#创建user表
cursor.execute('create table user (id varchar(20) primary key,name varchar(20))')
#插入一行记录
cursor.execute('insert into user (id,name) values (\'1\',\'Bob\')')
print(cursor.rowcount)
#提交事务
conn.commit()
cursor.close()
#运行查询
cursor = conn.cursor()
cursor.execute('select * from user where id =%s',('1',))
values = cursor.fetchall()
print(values)
#关闭cursor和connection
cursor.close()
conn.close()

#-----------------------------------------------------------使用SQLAlchemy
#形象的表示数据库（二维表）：用list[
#   							     User('1', 'Michael'),    一个tuple
#   								 User('2', 'Bob'),		  一个tuple
#   								 User('3', 'Adam')		  一个tuple
#								]
#python中的最有名的框架
#pip install sqlalchemy

#1、导入sqlalchemy，并初始化SBSession
#导入
from sqlalchemy import Column,String,create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#创建对象的框架
Base = declarative_base()
#定义User对象
class User(Base):
	#表的名字
	_tablename_ = 'user'
	#表的结构
	id = Column(String(20),primary_key=True)
	name = Column(String(20))

#初始化数据库连接
engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/test')	#'数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'

#创建DBSession类型
DBSession = sessionmaker(bind = engine)

# 创建session对象:
session = DBSession()
# 创建新User对象:
new_user = User(id='5', name='Bob')
# 添加到session:
session.add(new_user)
# 提交即保存到数据库:
session.commit()
# 关闭session:
session.close()

# 创建Session:
session = DBSession()
# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
user = session.query(User).filter(User.id=='5').one()
# 打印类型和对象的name属性:
print('type:', type(user))
print('name:', user.name)
# 关闭Session:
session.close()

#例如，如果一个User拥有多个Book，就可以定义一对多关系如下：

class User(Base):
    __tablename__ = 'user'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    # 一对多:
    books = relationship('Book')

class Book(Base):
    __tablename__ = 'book'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    # “多”的一方的book表是通过外键关联到user表的:
    user_id = Column(String(20), ForeignKey('user.id'))