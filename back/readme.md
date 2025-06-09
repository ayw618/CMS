


   app.py
   routes :  user.py  book.py   路由     
   api                          业务逻辑   
   operation：user_operation     数据操作
   model： user.py               数据模型类《===》数据库表映射


1、安装mysql
2、新建数据库
3、新建数据库表
4、 pip install  Flask-SQLAlchemy 
    pip install  pymysql

5、配置文件：配置数据库信息 ip port  dbname  root  password
6、新建数据模型类  models

登录接口
IP地址：http://127.0.0.1:5002/user/login
请求方式：POST
参数：
    username  用户名
    password  密码
返回值示例：
{
    ”code“：-1
    ”msg“：
    “data”：
}
字段含义：
code 状态码
msg 提示信息
data 业务数据

{
    "class_id":"a",
    "time":"2023-09-08 16:01:30.173295",
    "teacher_account";"1"
}
{
    "user_account":"111",
    "password":"111"
}
