from db_config import db_init as db


# 定义cms_teacher_class数据模型类
class CMSTeacherClass(db.Model):
    # 表名
    __tablename__ = 'cms_teacher_class'
    # 字段名称
    class_id = db.Column(db.String(32), primary_key=True)
    teacher_account = db.Column(db.String(32), primary_key=True)

    def __init__(self, teacher_account, class_id):
        self.class_id = class_id
        self.teacher_account = teacher_account

    def __repr__(self):
        return '<Teacher {}  Class {}>'.format(self.teacher_account, self.class_id)
