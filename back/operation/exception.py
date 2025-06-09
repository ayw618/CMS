from models.exception import CMSException
from models.score import CMSScore
from models.cms_class import CMSClass
import datetime
from datetime import timedelta
from datetime import datetime

from db_config import db_init as db
from db_config import app


class Exception_Operation():
    def __init__(self):
        self.fields = ['id', 'class_id', 'time', 'tag', 'link']
        self.exceptions = ['eating', 'chatting', 'bow_head', 'enter_exit', 'play_phone']

    def record(self, time, class_id, class_values, link):
        with app.app_context():
            for value in class_values:
                new_exception = CMSException(
                    time=time,
                    class_id=class_id,
                    tag=self.exceptions[int(value)],
                    link=link
                )
                print(new_exception)
                db.session.add(new_exception)

            result = db.session.commit()
            if result is None:
                print("success record")
                return 0
            else:
                print("error record")
                return 1

    def calculate_and_store_scores(self):
        tag_scores = {
            'eating': 2,
            'chatting': 3,
            'bow_head': 1,
            'enter_exit': 4,
            'play_phone': 5
        }

        # 获取班级列表从数据库
        classes = CMSClass.query.all()

        for class_info in classes:
            class_id = class_info.class_id

            # 获取当前日期
            today = datetime.now().date()

            # 获取班级的所有日期
            dates = [row[0].date() for row in db.session.query(CMSScore.time)
                .filter_by(class_id=class_id)
                .distinct()]

            # 计算每个日期的评分
            for date in dates + [today]:
                existing_score = CMSScore.query.filter_by(class_id=class_id, time=date).first()

                if existing_score:
                    print(f'Score for class {class_id} on {date} already exists. Updating score.')

                # 计算一天内的违纪记录
                start_time = datetime.combine(date, datetime.min.time())
                end_time = datetime.combine(date, datetime.max.time())

                total_score = 0

                # 抽取每个时间段的异常样本并计算评分
                segment_duration = timedelta(seconds=12)  # 每个时间段的持续时间

                current_time = start_time
                while current_time < end_time:
                    segment_start = current_time
                    segment_end = segment_start + segment_duration

                    exceptions = CMSException.query.filter_by(class_id=class_id) \
                        .filter(CMSException.time >= segment_start, CMSException.time <= segment_end) \
                        .all()

                    segment_score = 0

                    # 计算评分
                    for exception in exceptions:
                        tags = exception.tag.split(',')
                        score = sum(tag_scores.get(tag, 0) for tag in tags)
                        segment_score += score

                    total_score += segment_score
                    current_time += segment_duration

                if existing_score:
                    existing_score.score = total_score
                else:
                    # 创建一个新的CMSScore对象并保存到数据库
                    score_entry = CMSScore(time=date, class_id=class_id, score=total_score)
                    db.session.add(score_entry)

                result=db.session.commit()
                print(f'Score for class {class_id} on {date} calculated and stored: {total_score}')

        if result is None:
            print("success score")
            return 0
        else:
            print("error score")
            return 1

    def statistics_for_chart(self):
        # 获取所有classIds、dates和scores值从数据库
        data_from_db = db.session.query(CMSClass.class_id, CMSScore.time, CMSScore.score) \
            .join(CMSScore, CMSClass.class_id == CMSScore.class_id) \
            .all()

        # 从查询结果中提取classIds、dates和scores
        class_ids_from_db = sorted(list(set([row.class_id for row in data_from_db])))
        dates_from_db = sorted(list(set([row.time for row in data_from_db])))



        # 创建班级ID映射字典
        class_id_mapping = {class_id: f"{str(index + 1)}班" for index, class_id in enumerate(class_ids_from_db)}

        # 构建scores数据，使用嵌套列表的方式，每个内部列表表示一个班级的成绩数据
        scores_from_db = []
        for class_id in class_ids_from_db:
            class_scores = []
            for date in dates_from_db:
                # 在这里查找对应的分数，如果没有分数则添加None
                score = next((row.score for row in data_from_db if row.class_id == class_id and row.time == date), None)
                class_scores.append(score)
            scores_from_db.append(class_scores)



        # 提取日期的星期的英文缩写，日和月
        dates_from_db = [row.time.strftime("%a %d %b").replace(" 0001", "") for row in data_from_db]

        # 构建参数字典，使用映射后的班级ID和修改后的日期格式
        data = {
            'classIds': [class_id_mapping[class_id] for class_id in class_ids_from_db],
            # 'dates': list(set(dates_from_db)),  # 去重后的日期列表
            'dates': dates_from_db,
            'scores': scores_from_db
        }

        if data is None:
            print("error score")
            return 1
        else:
            print("success score")
            return data

    def tag_statistics(self):

        # 获取异常记录中的班级ID列表
        class_ids = db.session.query(CMSException.class_id).distinct().all()
        class_ids = [class_id[0] for class_id in class_ids]

        # 定义异常标签顺序
        tag_order = ['eating', 'chatting', 'bow_head', 'enter_exit', 'play_phone']

        # 统计每种行为的异常标签次数
        behavior_tags_counts = {}

        # 遍历每个标签并统计其异常次数
        for tag in tag_order:
            counts = []  # 用于存储每个班级的该标签的异常次数
            for class_id in class_ids:
                # 查询特定班级和标签的异常记录数量
                count = db.session.query(CMSException).filter(CMSException.class_id == class_id,
                                                              CMSException.tag == tag).count()
                counts.append(count)  # 将异常次数添加到列表中
            behavior_tags_counts[tag] = counts  # 将该标签的异常次数列表添加到字典中

        return behavior_tags_counts  # 返回包含每种行为标签的异常次数的字典

    def change_link(self):
        # 获取所有记录
        exceptions = CMSException.query.all()
        # 处理每个记录的链接字段
        for exception in exceptions:
            if exception.link and 'http://' in exception.link:
                # 分割链接并仅保留IP地址后面的部分
                parts = exception.link.split('/')
                new_link = '/' + '/'.join(parts[3:])

                # 更新记录的链接字段
                exception.link = new_link
        # 提交更改到数据库
        db.session.commit()



    def find_exception_by_id(self,id):
        # 根据序号查找异常帧记录
        exception = CMSException.query.get(id)
        print(exception)
        return exception

    def get_exceptions(self,start_index,end_index,per_page):
        # 返回需要显示的异常帧记录
        result = {}
        all_exceptions = CMSException.query.all()
        # 将查询结果转换为字典列表
        return_exceptions = []
        for exception in all_exceptions[start_index:end_index]:
            data = {
                "time": exception.time,
                "id": exception.id,
                "tag": exception.tag,
                "class_id": exception.class_id,
                "link": exception.link,
            }
            return_exceptions.append(data)
        result["exceptions"] = return_exceptions
        if len(all_exceptions) % per_page != 0:
            result["total_pages"] = len(all_exceptions) // per_page + 1
        else:
            result["total_pages"] = len(all_exceptions) // per_page
        return result

    def delete_exception(self,id):
        # 删除指定序号的异常帧记录
        input_exception = CMSException.query.get(id)
        db.session.delete(input_exception)
        db.session.commit()

    def delete_exception_by_class(self,class_id):
        # 删除某班级对应的所有异常帧记录
        exceptions = CMSException.query.filter_by(class_id = class_id).all()
        for exception in exceptions:
            db.session.delete(exception)
            db.session.commit()

    def count_exception_num_past_week(self):
        # 计算近一周的异常帧记录总数
        # 计算一周前的日期
        one_week_ago = datetime.now() - timedelta(days=7)
        # 使用 SQLAlchemy 查询数据库，筛选出发生时间在一周前之后的异常记录
        exceptions_past_week = CMSException.query.filter(CMSException.time >= one_week_ago).all()
        return len(exceptions_past_week)

    def count_exception_num(self, date):
        # 计算指定日期异常帧记录总数
        # 使用 SQLAlchemy 查询数据库，筛选出指定日期的异常记录
        exceptions_on_date = CMSException.query.filter(CMSException.time >= date,
                                                       CMSException.time < date + timedelta(days=1)).all()

        # 返回指定日期的异常记录数量
        return len(exceptions_on_date)

    def count_exceptions_for_previous_days(self):
        # 计算前天、昨天、今天的异常帧记录数量
        # 获取当前日期
        today = datetime.now().date()

        # 计算前天、昨天、今天的日期
        day_before_yesterday = today - timedelta(days=2)
        yesterday = today - timedelta(days=1)

        # 分别获取前天、昨天、今天的异常记录数量
        count_previous_day_before_yesterday = self.count_exception_num(day_before_yesterday)
        count_previous_yesterday = self.count_exception_num(yesterday)
        count_today = self.count_exception_num(today)

        return {
            'day_before_yesterday': count_previous_day_before_yesterday,
            'yesterday': count_previous_yesterday,
            'today': count_today
        }

    def calculate_tag_num(self):
        # 计算近500张异常帧记录中各异常行为的数量
        tag_num = {
            'eating': 0,
            'chatting': 0,
            'bow_head': 0,
            'enter_exit': 0,
            'play_phone': 0
        }

        # 从数据库中获取CMSException的后500条记录
        exceptions = CMSException.query.order_by(CMSException.id.desc()).limit(500).all()

        # 统计每个标签的数量
        tag_counts = {tag: 0 for tag in tag_num}
        for exception in exceptions:
            tag = exception.tag
            tag_num[tag] += 1
        return tag_num






