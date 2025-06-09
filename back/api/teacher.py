from operation.teacher import Teacher_Operation
from operation.teacher_class import TeacherClass_Operation
from db_config import db_init as db
from models.user import CMSUser
from models.teacher_class import CMSTeacherClass
from utils.data_process import Data_Process



def Teacher_ChangePassword (user_account,oldpassword,newpassword,recheckedpassword):
    result = {}
    t = Teacher_Operation()
    data = t.ChangePassword(user_account=user_account, OldPassword=oldpassword, NewPassword=newpassword,
                            RecheckedPassword=recheckedpassword)
    if data == 0:
        result["code"] = 0
        result['msg'] = "修改成功，新密码已设置"
    elif data == 1:
        result["code"] = 1
        result['msg'] = "原密码错误"
    elif data == 2:
        result["code"] = 2
        result['msg'] = "两次输入的新密码不一致"
    elif data == 3:
        result["code"] = 3
        result['msg'] = "账号异常"

    return result

def Teacher_login (user_account, password):
    result = {}
    t = Teacher_Operation()
    tc = TeacherClass_Operation()
    # data = t.Login(user_account=user_account)
    data = CMSUser.query.filter_by(user_account = user_account).first()

    if not data:
        result['code'] = 1
        result['msg'] = "登录失败，账号不存在"
    # elif data.state==1:
    #     result['code'] = 3 #实际为3
    #     result['msg'] = "登录失败，不能重复登录"
    elif data.password != password:
        result['code'] = 2
        result['msg'] = "登录失败，密码错误"
    elif data.role == 3:
        result['code'] = 4
        result['msg'] = "登录失败，管理员应该在网页端登录"
    elif data.password == password:
        t.change_state(user_account=user_account)
        result['user'] = Data_Process(data, t.fields, 1)

        # teacher = CMSUser.query.filter_by(user_account=user_account).first()
        print(data)
        teacher_class = CMSTeacherClass.query.filter_by(teacher_account=user_account).first()
        # data.state = 1
        if(data.role==1):
            result['code'] = 0
            result['msg'] = "教师登录成功"
            result['class_id'] = Data_Process(teacher_class, tc.fields, 1)
        elif(data.role==2):
            result['code'] = 10
            result['msg'] = "教导主任登录成功"
        # data 数据处理
        # db.session.commit()
        # a=Data_Process(data, t.fields, 1)
        # print(a)
    return result

def Teacher_logout(user_account):

    result = {}
    t=Teacher_Operation()
    t.change_state(user_account=user_account)
    result['code'] = 0
    result['msg'] = "退出成功"
    return result

    result = {}
    # t = Teacher_Operation()
    # data = t.Logout(user_account=user_account)
    # teacher = CMSUser.query.filter_by(user_account=user_account).first()
    # teacher = session.query(CMSUser).filter_by(user_account==user_account).with_for_update.first()
    # teacher = db.session.query(CMSUser).filter(CMSUser.user_account == user_account).with_for_update().first()
    #
    # print(teacher)
    # data = teacher.state
    # a = teacher.state
    # if data == 1:
    #     result["code"] = 0
    #     result['msg'] = "登出"
    #     print(teacher)
    # else:
    #     result['code'] = 1
    #     result['msg'] = "登出失败，账号未登录"
    # teacher.state = 0
    # b = teacher.state
    # db.session.commit()
    # return result




def Teacher_register(name, password, user_account, role, state):
    result = {}
    t = Teacher_Operation()
    data = t.register(name=name, password=password, user_account=user_account, role=role, state=state)

    if not data:
        result["code"] = 0
        result['msg'] = "注册成功"
    else:
        result['code'] = 1
        result['msg'] = "注册失败，账号已存在"

    return result


def Teacher_delete(user_account):
    result = {}
    t = Teacher_Operation()
    data = t.deregister(user_account=user_account)
    if not data:
        result['code'] = 0
        result['msg'] = "注销成功"
    else:
        result['code'] = 1
        result['msg'] = "注销失败，不存在该账号"

    return result

