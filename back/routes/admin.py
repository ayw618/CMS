from flask import Blueprint,request
import json

# 第1步
admin = Blueprint('admin', __name__)

from api.admin import *

# 第3步
@admin.route('/login', methods=['POST'])
def login():
    input_data = json.loads(request.data)
    user_account = input_data['user_account']
    password = input_data['password']
    data = Admin_login(user_account, password)
    return data


@admin.route('/logout', methods=['POST'])
def logout():
    input_data = json.loads(request.data)
    user_account = input_data['user_account']
    data = Admin_logout(user_account)
    return data


@admin.route('/changepassword',methods=['POST'])
def changepassword():
    input_data = json.loads(request.data)
    user_account = input_data['user_account']
    original_password = input_data['original_password']
    new_password = input_data['new_password']
    data = Admin_changepassword(user_account,original_password,new_password)
    return data

@admin.route('/register', methods=['POST'])
def register():
    input_data = json.loads(request.data)
    user_account = input_data['user_account']
    password = input_data['password']
    name = input_data['name']
    role = input_data['role']
    data = Admin_register(user_account, password,name,role)
    return data

@admin.route('/resetpassword',methods=['POST'])
def resetpassword():
    input_data = json.loads(request.data)
    teacher_account = input_data['teacher_account']
    new_password =input_data.get('new_password', "123")
    data = Admin_resetpassword(teacher_account,new_password)
    return data


@admin.route('/deregister', methods=['POST'])
def deregister():
    input_data = json.loads(request.data)
    user_account = input_data['user_account']
    data = Admin_deregister(user_account)
    return data

@admin.route('/showteachers', methods=['POST'])
def showteachers():
    input_data = json.loads(request.data)
    type = int(input_data.get('type', 1))
    page = int(input_data.get('page', 1))
    per_page = int(input_data.get('per_page', 20))
    data = Admin_showteachers(type,page,per_page)
    return data

@admin.route('/setpower', methods=['POST'])
def setpower():
    input_data = json.loads(request.data)
    user_account = input_data['user_account']
    new_role = input_data['role']
    data = Admin_setpower(user_account,new_role)
    return data

@admin.route('/createclass', methods=['POST'])
def createclass():
    input_data = json.loads(request.data)
    class_id = input_data['class_id']
    grade = input_data['grade']
    data = Admin_createclass(class_id,grade)
    return data

@admin.route('/changegrade', methods=['POST'])
def changegrade():
    input_data = json.loads(request.data)
    class_id = input_data['class_id']
    grade = input_data['grade']
    data = Admin_changegrade(class_id,grade)
    return data

@admin.route('/deleteclass', methods=['POST'])
def deleteclass():
    input_data = json.loads(request.data)
    class_id = input_data['class_id']
    data = Admin_deleteclass(class_id)
    return data

@admin.route('/assignclass', methods=['POST'])
def assignclass():
    input_data = json.loads(request.data)
    class_id = input_data['class_id']
    teacher_account = input_data['teacher_account']
    data = Admin_assignclass(teacher_account,class_id)
    return data

@admin.route('/unassignclass', methods=['POST'])
def unassignclass():
    input_data = json.loads(request.data)
    class_id = input_data['class_id']
    teacher_account = input_data['teacher_account']
    data = Admin_unassignclass(teacher_account,class_id)
    return data

@admin.route('/showbrowses', methods=['POST'])
def showbrowses():
    input_data = json.loads(request.data)
    page = int(input_data.get('page', 1))
    per_page = int(input_data.get('per_page', 20))
    data = Admin_showbrowses(page,per_page)
    return data

@admin.route('/showclasses', methods=['POST'])
def showclasses():
    input_data = json.loads(request.data)
    page = int(input_data.get('page', 1))
    per_page = int(input_data.get('per_page', 20))
    data = Admin_showclasses(page,per_page)
    return data

@admin.route('/showclassstudents', methods=['POST'])
def showclassstudents():
    input_data = json.loads(request.data)
    class_id = input_data['class_id']
    page = int(input_data.get('page', 1))
    per_page = int(input_data.get('per_page', 20))
    data = Admin_showclassstudents(class_id,page,per_page)
    return data

@admin.route('/showallstudents', methods=['POST'])
def showallstudents():
    input_data = json.loads(request.data)
    page = int(input_data.get('page', 1))
    per_page = int(input_data.get('per_page', 20))
    data = Admin_showallstudents(page,per_page)
    return data

@admin.route('/createstudent', methods=['POST'])
def createstudent():
    input_data = json.loads(request.data)
    student_id = input_data['student_id']
    class_id = input_data['class_id']
    name = input_data['name']
    gender = input_data['gender']
    data = Admin_createstudent(student_id,class_id,name,gender)
    return data

@admin.route('/deletestudent', methods=['POST'])
def deletestudent():
    input_data = json.loads(request.data)
    student_id = input_data['student_id']
    data = Admin_deletestudent(student_id)
    return data

@admin.route('/showexceptions', methods=['POST'])
def showexceptions():
    input_data = json.loads(request.data)
    page = int(input_data.get('page', 1))
    per_page = int(input_data.get('per_page', 20))
    data = Admin_showexceptions(page,per_page)
    return data

@admin.route('/deleteexception', methods=['POST'])
def deleteexception():
    input_data = json.loads(request.data)
    id = input_data['id']
    data = Admin_deleteexception(id)
    return data

@admin.route('/showstatistics', methods=['GET'])
def showstatistics():
    data = Admin_showstatistics()
    return data
