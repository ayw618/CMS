#user 既是管理员，又是老师，但是一个类分成两个文件，teacher和admin
from models.browse import CMSBrowse
from db_config import db_init as db
from datetime import datetime, timedelta


class Browse_Operation():

    def __init__(self):
        self.fields = ['id', 'time', 'teacher_id', 'class_id']

    def record(self, teacher_account, time, class_id):
        new_browse = CMSBrowse(
            time=time,
            teacher_account=teacher_account,
            class_id=class_id
        )
        db.session.add(new_browse)
        result= db.session.commit()
        if result is None:
            print("success record")
            return 0
        else:
            print("error record")
            return 1

    def get_browsing_records(self,start_index,end_index,per_page):
        # 获取指定区间的浏览记录
        result = {}
        browsing_records = CMSBrowse.query.all()
        # 将查询结果转换为字典列表
        browses = []
        for browse_record in browsing_records[start_index:end_index]:
            browse = {
                "time": browse_record.time,
                "id": browse_record.id,
                "teacher_account": browse_record.teacher_account,
                "class_id": browse_record.class_id,
            }
            browses.append(browse)
        result["browses"] = browses
        if len(browsing_records) % per_page != 0:
            result["total_pages"] = len(browsing_records) // per_page + 1
        else:
            result["total_pages"] = len(browsing_records) // per_page
        return result

    def find_browse_by_teacher(self,teacher_account):
        # 查找某个教师的第一条浏览记录
        browse = CMSBrowse.query.filter_by(teacher_account=teacher_account).first()
        print(browse)
        return browse

    def delete_browse_by_teacher(self, teacher_account):
        # 删除某个教师的所有浏览记录
        browses = CMSBrowse.query.filter_by(teacher_account=teacher_account).all()
        for browse in browses:
            db.session.delete(browse)
            db.session.commit()

    def count_browse_num_past_week(self):
        # 计算近一周的浏览记录数量
        one_week_ago = datetime.now() - timedelta(days=7)
        # 使用 SQLAlchemy 查询数据库，筛选出发生时间在一周前之后的异常记录
        browse_past_week = CMSBrowse.query.filter(CMSBrowse.time >= one_week_ago).all()
        return len(browse_past_week)

    def count_browse_num(self, date):
        # 使用 SQLAlchemy 查询数据库，筛选出指定日期的教师浏览记录
        exceptions_on_date = CMSBrowse.query.filter(CMSBrowse.time >= date,
                                                    CMSBrowse.time < date + timedelta(days=1)).all()

        # 返回指定日期的教师浏览记录数量
        return len(exceptions_on_date)


    def count_browse_for_previous_days(self):
        # 计算前天、昨天、今天的浏览记录数量
        # 获取当前日期
        today = datetime.now().date()

        # 计算前天、昨天、今天的日期
        day_before_yesterday = today - timedelta(days=2)
        yesterday = today - timedelta(days=1)

        # 分别获取前天、昨天、今天的教师浏览记录数量
        count_previous_day_before_yesterday = self.count_browse_num(day_before_yesterday)
        count_previous_yesterday = self.count_browse_num(yesterday)
        count_today = self.count_browse_num(today)

        return {
            'day_before_yesterday': count_previous_day_before_yesterday,
            'yesterday': count_previous_yesterday,
            'today': count_today
        }









