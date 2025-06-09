from db_config import db_init as db

# 定义user数据模型类

class CMSUser(db.Model):
    __tablename__ = 'cms_user'


    user_account = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(32), nullable=True)
    name = db.Column(db.String(128), nullable=True)
    role = db.Column(db.Integer, nullable=True, autoincrement=False)
    state = db.Column(db.Integer, nullable=True)

    def __init__(self, user_account, password,name,role,state):
        self.user_account = user_account
        self.password = password
        self.name = name
        self.role = role
        self.state = state

    def __repr__(self):
        return f'<User account: {self.user_account}, Password: {self.password}, Name: {self.name}, Role: {self.role}, State: {self.state}>'
