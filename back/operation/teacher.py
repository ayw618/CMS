#user 既是管理员，又是老师，但是一个类分成两个文件，teacher和admin


from models.user import CMSUser
from db_config import db_init as db


class Teacher_Operation():

    def __init__(self):
        self.fields = ['user_account', 'name', 'password', 'role', 'state']

    def register(self, name, password, user_account, role, state):
        teacher = CMSUser.query.filter_by(user_account = user_account).first()
        # 如果找到用户，则结束
        if teacher:
            print("注册失败，账号已存在.")
            return 1
        else:
            teacher = CMSUser(name=name, password=password, user_account=user_account, role=role, state=state)
            db.session.add(teacher)
            # 提交数据到数据库中
            db.session.commit()
            print("注册成功.")
            return 0

    def deregister(self, user_account):
        # 查询具有特定用户账号的教师用户
        teacher = CMSUser.query.filter_by(user_account=user_account).first()
        # 如果找到用户，则删除该用户
        if teacher:
            db.session.delete(teacher)
            db.session.commit()
            print(f"用户 {user_account} 已删除。")
            return 0
        else:
            print(f"未找到用户 {user_account}。")
            return 1

    def ChangePassword(self, user_account, OldPassword, NewPassword, RecheckedPassword):
        teacher = CMSUser.query.filter_by(user_account = user_account).first()
        if not teacher:
            print("教师账号异常！")
            return 3
        elif OldPassword != teacher.password:
            print("重新输入的原密码错误")
            return 1
        elif NewPassword != RecheckedPassword:
            print("新输入的两次密码不一致")
            return 2
        else:
            teacher.password = NewPassword
            db.session.commit()
            print("修改成功")
            return 0


    def Login(self,user_account):
        # 代码实现放在api中

         return


    def Logout(self,user_account):
        # 代码实现放在api中

        return


    def change_state(self,user_account):
        teacher = CMSUser.query.get(user_account)
        if teacher.state == 0:
            teacher.state=1
        else:
            teacher.state = 0
        db.session.commit()









