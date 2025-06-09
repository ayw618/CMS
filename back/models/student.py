from db_config import db_init as db

# 定义cms_student数据模型类
class CMSStudent(db.Model):
    __tablename__ = 'cms_student'

    student_id = db.Column(db.String(32), primary_key=True)
    class_id = db.Column(db.String(32))
    name = db.Column(db.String(64))
    gender = db.Column(db.String(32))


    def __init__(self, student_id, class_id,name, gender):
        self.student_id = student_id
        self.class_id = class_id
        self.name = name
        self.gender = gender

    def __repr__(self):
        return f'<CMSStudent ID: {self.student_id}, Name: {self.name}, Class ID: {self.class_id}>'