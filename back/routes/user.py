# user:login  registerchangeinfo  de
from flask import Blueprint,request
import json
# 第1步
user = Blueprint('user', __name__)


from api.user import *

@user.route('/register', methods=['POST'])
def register():
    data = json.loads(request.data)
    user_account = data['user_account']
    password = data['password']
    name = data['name']
    role = data['role']
    state = data['state']

    result = User_register(user_account=user_account, password=password, name=name,role= role, state=state)
    return result

#删除账户
@user.route('/deregister',methods=['POST'])
def deluser():
    data=json.loads(request.data)
    user_account = data['user_account']
    result = User_delete(user_account = user_account)
    return result



