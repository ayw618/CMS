from models.student import CMSStudent
from db_config import db_init as db


class Student_Operation():
    def __init__(self):
        self.fields = ['id', 'time', 'teacher_account', 'class_id']

    def create_student(self, student_id, class_id, name, gender):
        # 创建学生信息
        new_student = CMSStudent(student_id, class_id,name,gender)
        db.session.add(new_student)
        db.session.commit()

    def find_student_by_id(self,student_id):
        # 根据学号查找学生
        student = CMSStudent.query.get(student_id)
        print(student)
        return student

    def find_student_by_class(self,class_id):
        # 查找某班第一个学生
        student = CMSStudent.query.filter_by(class_id=class_id).first()
        print(student)
        return student

    def delete_student(self, student_id):
        # 删除指定学号的学生信息
        input_student = CMSStudent.query.get(student_id)
        db.session.delete(input_student)
        db.session.commit()

    def get_students_by_class(self, class_id, start_index, end_index, per_page):
        # 返回指定班级要显示的学生
        result = {}
        all_students = CMSStudent.query.filter_by(class_id=class_id).all()
        # 将查询结果转换为字典列表
        students = []
        for student_data in all_students[start_index:end_index]:
            student = {
                "class_id": student_data.class_id,
                "student_id": student_data.student_id,
                "name": student_data.name,
                "gender": student_data.gender
            }
            students.append(student)
        result["students"] = students
        result["student_num"] = len(all_students)
        if len(all_students) % per_page != 0:
            result["total_pages"] = len(all_students) // per_page + 1
        else:
            result["total_pages"] = len(all_students) // per_page
        return

    def get_all_students(self, start_index, end_index, per_page):
        # 返回要显示的学生
        result = {}
        all_students = CMSStudent.query.all()
        # 将查询结果转换为字典列表
        students = []
        for student_data in all_students[start_index:end_index]:
            student = {
                "class_id": student_data.class_id,
                "student_id": student_data.student_id,
                "name": student_data.name,
                "gender": student_data.gender
            }
            students.append(student)
        result["students"] = students
        result["student_num"] = len(all_students)
        if len(all_students) % per_page != 0:
            result["total_pages"] = len(all_students) // per_page + 1
        else:
            result["total_pages"] = len(all_students) // per_page
        return result

    def count_student_num(self):
        # 计算学生总数
        cms_student = CMSStudent.query.all()
        return len(cms_student)

