from db_config import db_init as db

# 定义class数据模型类
class CMSClass(db.Model):
    __tablename__ = 'cms_class'

    class_id = db.Column(db.String(32), primary_key=True,nullable=False)
    grade=db.Column(db.String(32),nullable=True, default=None)

    def __init__(self, class_id, grade):
        self.class_id = class_id
        self.grade = grade

    def __repr__(self):
        return f'<CMSClass ID: {self.class_id}, Grade: {self.grade}>'
