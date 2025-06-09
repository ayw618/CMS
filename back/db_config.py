from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.orm import Session

app = Flask(__name__)
# 数据库类型 ip  port root  密码
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zly123@127.0.0.1:3306/classroom_monitor_sys'


db_init = SQLAlchemy(app)



