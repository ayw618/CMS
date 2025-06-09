from models.teacher_class import  CMSTeacherClass
from db_config import db_init as db


class TeacherClass_Operation():
    def __init__(self):
        self.fields = ['class_id', 'teacher_account']

    def find_teacherclass(self,teacher_account,class_id):
        # 根据教师账号、班级号，查找对应的教师、班级关联
        cms_class = CMSTeacherClass.query.filter_by(teacher_account=teacher_account, class_id=class_id).first()
        print(cms_class)
        return cms_class

    def find_teacherclass_by_teacher(self, teacher_account):
        # 查找和某教师账号有关联的教师、班级关联
        cms_class = CMSTeacherClass.query.filter_by(teacher_account=teacher_account).first()
        print(cms_class)
        return cms_class

    def find_teacher_by_class(self, class_id):
        # 查找和某班级号有关联的教师、班级关联
        cms_class = CMSTeacherClass.query.filter_by(class_id=class_id).first()
        if cms_class is not None:
            teacher_account = cms_class.teacher_account
            print(teacher_account)
            return teacher_account
        else:
            return ""

    def assign_class(self,teacher_account,class_id):
        # 根据教师账号、班级号，创建对应的教师、班级关联
        new_data = CMSTeacherClass(teacher_account,class_id)
        db.session.add(new_data)
        db.session.commit()

    def unassign_class(self, teacher_account, class_id):
        # 根据教师账号、班级号，删除对应的教师、班级关联
        cms_class = CMSTeacherClass.query.filter_by(teacher_account=teacher_account, class_id=class_id).first()
        if cms_class is not None:
            db.session.delete(cms_class)
            db.session.commit()

