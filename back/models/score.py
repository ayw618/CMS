from db_config import db_init as db

# 定义score数据模型类
class CMSScore(db.Model):
    __tablename__ = 'cms_score'

    id = db.Column(db.Integer,nullable=False, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, nullable=True, default=None)
    class_id = db.Column(db.String(32), nullable=True, default=None)
    score = db.Column(db.Float, nullable=True, default=None)


    def __repr__(self):
        return f'<CMSScore ID: {self.id}, Class ID: {self.class_id}, Score: {self.score}>'
