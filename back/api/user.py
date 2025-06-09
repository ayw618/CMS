from  operation.user import  User_Operation
from utils.data_process import  Data_Process


def User_register(name, password, user_account, role, state):
     result={}
     u = User_Operation()
     data = u.register(name=name, password=password, user_account=user_account, role=role, state = state)
     
     if not data:
          result["code"] = 0
          result['msg'] = "注册成功"
     else:
          result['code'] = 1
          result['msg'] = "注册失败，账号已存在"
     
     return result


def User_delete(user_account):
     result = {}
     u = User_Operation()
     data = u.deluser(user_account = user_account)
     if not data:
          result['code'] = 0
          result['msg'] = "注销成功"
     else:
          result['code'] = 1
          result['msg'] = "注销失败，不存在该账号"

     return result
