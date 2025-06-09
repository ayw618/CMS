from db_config import db_init as db

# 定义browse数据模型类

class CMSBrowse(db.Model):
    __tablename__ = 'cms_browse'

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, nullable=True, default=None)
    teacher_account = db.Column(db.String(32), nullable=True, default=None)
    class_id = db.Column(db.String(32), nullable=True, default=None)


    def __repr__(self):
        return f'<CMSBrowse ID: {self.id}, Time: {self.time}>'
