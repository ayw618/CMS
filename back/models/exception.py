from db_config import db_init as db

class CMSException(db.Model):
    __tablename__ = 'cms_exception'

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    class_id = db.Column(db.String(32), nullable=True, default=None)
    time = db.Column(db.DateTime, nullable=True, default=None)
    tag = db.Column(db.String(256), nullable=True, default=None)
    link = db.Column(db.String(256), nullable=True, default=None)



    def __repr__(self):
        return f'<CMSException ID: {self.id}, Class ID: {self.class_id}, Time: {self.time}>'
