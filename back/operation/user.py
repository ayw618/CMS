from models.user import  CMSUser
from db_config import  db_init as db
from sqlalchemy import or_

class User_Operation():
    # def all(self):
    #     # excute:select * from users
    #     data = Users.query.all()
    #     return  data
    def __init__(self):
        self.fields = ['user_account','name','role']

    def count_teacher_num(self):
        # 计算教师总数
        teachers = CMSUser.query.filter(or_(CMSUser.role == 1, CMSUser.role == 2)).all()
        return len(teachers)

    def get_class_teachers(self,start_index,end_index,per_page):
        # 获取要显示的班主任
        result = {}
        teachers = CMSUser.query.filter_by(role=1).all()
        # 将查询结果转换为字典列表
        class_teachers = []
        for teacher in teachers[start_index:end_index]:
            user_data = {
                "user_account": teacher.user_account,
                "name": teacher.name,
                "role": teacher.role,
                "state": teacher.state
            }
            class_teachers.append(user_data)
        result["teachers"]=class_teachers
        result["teacher_num"] = len(teachers)
        if len(teachers) % per_page != 0:
            result["total_pages"]=len(teachers) // per_page + 1
        else:
            result["total_pages"]=len(teachers) // per_page
        return result

    def get_directors(self,start_index,end_index,per_page):
        # 获取要显示的教导主任
        result = {}
        directors = CMSUser.query.filter_by(role=2).all()
        # 将查询结果转换为字典列表
        directors_teacher = []
        for director in directors[start_index:end_index]:
            user_data = {
                "user_account": director.user_account,
                "name": director.name,
                "role": director.role,
                "state": director.state
            }
            directors_teacher.append(user_data)
        result["teachers"] = directors_teacher
        result["teacher_num"] = len(directors)
        if len(directors) % per_page != 0:
            result["total_pages"] = len(directors) // per_page + 1
        else:
            result["total_pages"] = len(directors) // per_page
        return result

    def get_all_teachers(self,start_index,end_index,per_page):
        # 获取要显示的教师
        result = {}
        teachers = CMSUser.query.filter(or_(CMSUser.role == 1, CMSUser.role == 2)).all()
        all_teachers = []
        for teacher in teachers[start_index:end_index]:
            user_data = {
                "user_account": teacher.user_account,
                "name": teacher.name,
                "role": teacher.role,
                "state": teacher.state
            }
            all_teachers.append(user_data)
        result["teachers"] = all_teachers
        result["teacher_num"] = len(teachers)
        if len(teachers) % per_page != 0:
            result["total_pages"] = len(teachers) // per_page + 1
        else:
            result["total_pages"] = len(teachers) // per_page
        return result

    def find_user_by_account(self,user_account):
        # 根据用户账号查找用户
        user = CMSUser.query.get(user_account)
        print(user)
        return user


    def change_state(self,user_account):
        # 改变用户在线状态
        user = CMSUser.query.get(user_account)
        if user.state == 0:
            user.state = 1
        else:
            user.state = 0
        db.session.commit()

    def change_pwd(self, user_account, new_password):
        # 用新密码替换指定用户的原密码
        user = CMSUser.query.get(user_account)
        user.password = new_password
        db.session.commit()

    def register(self,user_account,password,name,role):
        # 注册新的用户
        new_user = CMSUser(user_account,password,name,role,0)
        db.session.add(new_user)
        db.session.commit()

    def reset_password(self, teacher_account, new_password):
        # 重新设置教师密码
        user = CMSUser.query.get(teacher_account)
        user.password = new_password
        db.session.commit()

    def deregister(self,user_account):
        # 注销指定账号的用户
        user = CMSUser.query.get(user_account)
        db.session.delete(user)
        db.session.commit()

    def set_power(self,user_account,role):
        # 为教师设置权限
        user = CMSUser.query.get(user_account)
        user.role = role
        db.session.commit()