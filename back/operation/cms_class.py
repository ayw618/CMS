from models.cms_class import CMSClass
from operation.teacher_class import TeacherClass_Operation
from db_config import db_init as db


class Class_Operation():
    def __init__(self):
        self.fields = ['class_id', 'grade']

    def find_class_by_id(self,class_id):
        # 根据班级号查找班级
        cms_class = CMSClass.query.get(class_id)
        print(cms_class)
        return cms_class

    def create_class(self,class_id,grade):
        # 创建班级信息
        new_class = CMSClass(class_id,grade)
        db.session.add(new_class)
        db.session.commit()

    def change_grade(self,class_id,grade):
        # 更改某班级的年级信息
        cms_class = CMSClass.query.get(class_id)
        cms_class.grade = grade
        db.session.commit()

    def delete_class(self,class_id):
        # 删除班级信息
        input_class = CMSClass.query.get(class_id)
        db.session.delete(input_class)
        db.session.commit()

    def get_classes(self,start_index,end_index,per_page):
        # 获取要显示的班级
        result = {}
        all_classes = CMSClass.query.all()
        tc = TeacherClass_Operation()
        # 将查询结果转换为字典列表
        return_classes = []
        for class_iterator in all_classes[start_index:end_index]:
            teacher_account = tc.find_teacher_by_class(class_iterator.class_id)
            one_class = {
                "grade": class_iterator.grade,
                "class_id": class_iterator.class_id,
                "teacher_account":teacher_account
            }
            return_classes.append(one_class)
        result["classes"] = return_classes
        result["class_num"] = len(all_classes)
        if len(all_classes) % per_page != 0:
            result["total_pages"] = len(all_classes) // per_page + 1
        else:
            result["total_pages"] = len(all_classes) // per_page
        return result

    def count_class_num(self):
        # 计算班级总数
        cms_class = CMSClass.query.all()
        return len(cms_class)
