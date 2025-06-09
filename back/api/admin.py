from operation.user import User_Operation
from operation.cms_class import Class_Operation
from operation.browse import Browse_Operation
from operation.teacher_class import TeacherClass_Operation
from operation.exception import Exception_Operation
from operation.student import Student_Operation
from utils.data_process import Data_Process
from flask import jsonify


def Admin_login(user_account, input_password):
    # 管理员登录业务接口封装
    result = {}
    u = User_Operation()
    data = u.find_user_by_account(user_account)

    # 输入账号不存在的登录失败，账号存在的情况进一步判断
    if data is not None:
        # 输入账号不是管理员身份的登录失败，其他情况进一步判断
        if data.role == 3:
            real_password = data.password
            # 输入密码错误的登录失败，其他情况进一步判断
            if real_password != input_password:
                result['code'] = 2
                result['msg'] = "登录失败，密码错误"
            else:
                # 已经重复登录的登录失败，否则登录成功
                if data.state == 1:
                    result['code'] = 3
                    result['msg'] = "登录失败，不能重复登录"
                else:
                    result['code'] = 0
                    result['msg'] = "登录成功"
                    # data 数据处理
                    result['user'] = Data_Process(data, u.fields, 1)
                    u.change_state(user_account)   # 登录要改变在线状态 0 --> 1
        else:
            result['code'] = 4
            result['msg'] = "登录失败，教师账号不能登录管理员系统"
    else:
        result['code'] = 1
        result['msg'] = "登录失败，账号不存在"
    return result


def Admin_changepassword(user_account,input_original_password,new_password):
    # 管理员修改密码业务接口封装
    result = {}
    u = User_Operation()
    data = u.find_user_by_account(user_account)
    real_original_password = data.password
    # 原密码正确时，成功修改密码
    if real_original_password == input_original_password:
        u.change_pwd(user_account,new_password)
        result['code'] = 0
        result['msg'] = "密码修改成功"
    else:
        # 原密码错误时，修改失败
        result['code'] = 1
        result['msg'] = "修改失败，原密码错误"
    return result

def Admin_logout(user_account):
    # 管理员登出业务接口封装
    result = {}
    u = User_Operation()
    u.change_state(user_account)  # 登出要改变在线状态 1 --> 0
    result['code'] = 0
    result['msg'] = "退出成功"
    return result

def Admin_register(user_account, password, name, role):
    # 管理员注册教师账号业务接口封装
    result = {}
    u = User_Operation()
    user = u.find_user_by_account(user_account)
    # 新注册账号不能与数据库中已存在账号重复
    if user is not None:
        result['code'] = 1
        result['msg'] = "注册失败，账号已存在"
    else:
        result['code'] = 0
        result['msg'] = "注册成功"
        u.register(user_account, password, name, role)
        new_user = u.find_user_by_account(user_account)
        result['user'] = Data_Process(new_user, u.fields, 1)
    return result

def Admin_resetpassword(teacher_account,new_password):
    # 管理员重新设置教师密码业务接口封装
    result = {}
    u = User_Operation()
    data = u.find_user_by_account(teacher_account)
    # 要重置密码的教师账号不存在时，重置失败
    if data is None:
        result['code'] = 1
        result['msg'] = "重置失败，输入教师账号不存在"
    else:
        u.reset_password(teacher_account,new_password)
        result['code'] = 0
        result['msg'] = "密码重置成功"
    return result

def Admin_deregister(user_account):
    # 管理员注销教师账号业务接口封装
    result = {}
    u = User_Operation()
    tc = TeacherClass_Operation()
    b = Browse_Operation()
    user = u.find_user_by_account(user_account)
    # 输入教师账号不存在时注销失败，否则继续判断
    if user is None:
        result['code'] = 1
        result['msg'] = "注销失败，不存在该账号"
    else:
        # 只能注销班主任或教导主任的账号
        if user.role != 3:
            cms_class = tc.find_teacherclass_by_teacher(user_account)
            browse = b.find_browse_by_teacher(user_account)
            if cms_class is not None:
                # 注销前，将分配给该班级的教师取消分配
                class_id = cms_class.class_id
                tc.unassign_class(user_account, class_id)
            if browse is not None:
                # 注销前，删除教师查看该班级监控的浏览记录
                b.delete_browse_by_teacher(user_account)
            result['code'] = 0
            result['msg'] = "注销成功"
            u.deregister(user_account)
        else:
            # 不能注销其他管理员的账号
            result['code'] = 2
            result['msg'] = "注销失败，不能注销其他管理员账号"
    return result

def Admin_setpower(user_account, role):
    # 管理员设置教师权限业务接口封装
    result = {}
    u = User_Operation()
    user = u.find_user_by_account(user_account)
    if user is None:
        # 输入账号不存在时操作失败
        result['code'] = 1
        result['msg'] = "修改失败，不存在该账号"
    else:
        if user.role != role:
            # 新权限和旧权限不同时修改成功
            result['code'] = 0
            result['msg'] = "修改成功"
            u.set_power(user_account, role)  # 设置新权限
            new_user_info = u.find_user_by_account(user_account)
            result['user'] = Data_Process(new_user_info, u.fields, 1)
        else:
            result['code'] = 2
            result['msg'] = "修改无效，新权限与之前相同"
    return result

def Admin_createclass(class_id,grade):
    # 管理员创建班级信息业务接口封装
    result = {}
    c = Class_Operation()
    class_data = c.find_class_by_id(class_id)
    # 输入班级号和已有班级号不重复时创建成功，否则失败
    if class_data is None:
        result['code'] = 0
        result['msg'] = "创建成功"
        c.create_class(class_id,grade)
    else:
        result['code'] = 1
        result['msg'] = "创建失败，班级号已存在"
    return result

def Admin_changegrade(class_id, grade):
    # 管理员更改某班的年级信息业务接口封装
    result = {}
    c = Class_Operation()
    data = c.find_class_by_id(class_id)
    # 前端会在班级名单选择班级进行修改，故默认class_id在数据库中存在
    if data.grade != grade:
        # 输入年级与原年级不同时，修改成功
        c.change_grade(class_id, grade)
        result['code'] = 0
        result['msg'] = "修改成功"
    else:
        # 输入年级与原年级相同时，修改无效
        result['code'] = 1
        result['msg'] = "无效修改，输入年级与原来相同"
    return result
def Admin_deleteclass(class_id):
    # 管理员删除班级业务接口封装
    result = {}
    c = Class_Operation()
    s = Student_Operation()
    class_data = c.find_class_by_id(class_id)
    if class_data is None:
        # 输入班级号不存在时，删除失败
        result['code'] = 1
        result['msg'] = "删除失败，班级号不存在"
    else:
        student = s.find_student_by_class(class_id)
        # 删除班级存在学生时，要先删除该班级所有学生信息，之后才能删除该班级信息
        if student is None:
            tc = TeacherClass_Operation()
            teacher_account = tc.find_teacher_by_class(class_id)
            # 成功删除前，自动解除该班级与班主任的关联
            if teacher_account is not None:
                tc.unassign_class(teacher_account,class_id)
            e = Exception_Operation()
            # 成功删除前，自动删除属于该班级的异常帧记录
            e.delete_exception_by_class(class_id)
            result['code'] = 0
            result['msg'] = "删除成功"
            c.delete_class(class_id)
        else:
            result['code'] = 2
            result['msg'] = "删除失败，班级删除前应先删除该班级的学生"
    return result

def Admin_assignclass(teacher_account,class_id):
    # 管理员给教师分配管理的班级业务接口封装
    result = {}
    u = User_Operation()
    tc = TeacherClass_Operation()
    c = Class_Operation()
    teacher = u.find_user_by_account(teacher_account)
    cms_class = c.find_class_by_id(class_id)
    # 输入教师账号为空，提示输入教师账号
    if teacher_account == "":
        result['code'] = 6
        result['msg'] = "请输入教师账号"
        return result
    # 输入教师账号但是该账号不存在，分配失败
    if teacher is None:
        result['code'] = 4
        result['msg'] = "分配失败，输入教师账号不存在"
    else:
        # 输入班级账号不存在时，分配失败
        if cms_class is None:
            result['code'] = 3
            result['msg'] = "分配失败，输入班级号不存在"
        else:
            data = tc.find_teacherclass(teacher_account,class_id)
            if data is not None:
                # 输入班级和老师原本已关联，无效分配
                result['code'] = 1
                result['msg'] = "无效分配，输入的班级与老师已关联"
            else:
                if teacher.role == 2:
                    # 教导主任默认拥有所有班级管理权限，不用分配
                    result['code'] = 5
                    result['msg'] = "分配失败，无需给教导主任分配班级"
                else:
                    teacher_class_data = tc.find_teacherclass_by_teacher(teacher_account)
                    if teacher_class_data is None:
                        # 成功分配
                        result['code'] = 0
                        result['msg'] = "班级分配成功"
                        tc.assign_class(teacher_account, class_id)  # 执行分配操作
                        teacher_class_data = tc.find_teacherclass(teacher_account, class_id)
                        result['teacher_class'] = Data_Process(teacher_class_data, tc.fields, 1)
                    else:
                        # 班主任管理不能多于一个
                        result['code'] = 2
                        result['msg'] = "分配失败，班主任最多只能分配一个班级"
    return result

def Admin_unassignclass(teacher_account,class_id):
    # 管理员取消给教师分配班级业务接口封装
    result = {}
    u = User_Operation()
    tc = TeacherClass_Operation()
    c = Class_Operation()
    teacher = u.find_user_by_account(teacher_account)
    cms_class = c.find_class_by_id(class_id)
    # 前端传来teacher_account为""时，说明该班级原本没有班主任
    if teacher_account == "":
        result['code'] = 4
        result['msg'] = "原本未分配"
        return result
    # 教师账号不为空，但是不存在时，操作失败
    if teacher is None:
        result['code'] = 2
        result['msg'] = "分配失败，输入教师账号不存在"
    else:
        # 输入班级号不存在时操作失败否则继续判断
        if cms_class is None:
            result['code'] = 1
            result['msg'] = "分配失败，输入班级号不存在"
        else:
            teacher_class_data = tc.find_teacherclass(teacher_account, class_id)
            # 输入班级与老师原本未关联时操作无效，否则取消其关联
            if teacher_class_data is None:
                result['code'] = 3
                result['msg'] = "取消分配无效，输入班级与老师原本未关联"
            else:
                tc.unassign_class(teacher_account,class_id)  # 取消分配操作
                result['code'] = 0
                result['msg'] = "取消分配成功"
    return result

def Admin_showteachers(type,page,per_page):
    # 管理员查看指定类型的教师名单业务接口封装
    result = {}
    u = User_Operation()
    # 计算所展示页面的教师的起止索引
    start_index = (page - 1) * per_page
    end_index = page * per_page
    if type == 1:
        # 显示所有教师的名单
        result["code"]=0
        result["msg"]="显示成功"
        return_data = u.get_all_teachers(start_index,end_index,per_page)
        result["data"] = return_data["teachers"]
        result["total_pages"] = return_data["total_pages"]
        result["teacher_num"] = return_data["teacher_num"]
    elif type == 2:
        # 显示所有班主任的名单
        result["code"]=0
        result["msg"]="显示成功"
        return_data = u.get_class_teachers(start_index,end_index,per_page)
        result["data"] = return_data["teachers"]
        result["total_pages"] = return_data["total_pages"]
        result["teacher_num"] = return_data["teacher_num"]
    elif type == 3:
        # 显示所有教导主任的名单
        result["code"]=0
        result["msg"]="显示成功"
        return_data = u.get_directors(start_index,end_index,per_page)
        result["data"] = return_data["teachers"]
        result["total_pages"] = return_data["total_pages"]
        result["teacher_num"] = return_data["teacher_num"]
    else:
        result["code"] = 1
        result["msg"] = "显示失败，输入参数不合法"
    return jsonify(result)

def Admin_showbrowses(page,per_page):
    # 管理员查看教师浏览记录业务接口封装
    result = {}
    b = Browse_Operation()
    start_index = (page - 1) * per_page
    end_index = page * per_page
    result["code"]=0
    result["msg"]="显示成功"
    return_data = b.get_browsing_records(start_index,end_index,per_page)
    result["data"] = return_data["browses"]
    result["total_pages"] = return_data["total_pages"]
    return jsonify(result)

def Admin_showclasses(page,per_page):
    # 管理员查看班级名单业务接口封装
    result = {}
    c = Class_Operation()
    start_index = (page - 1) * per_page
    end_index = page * per_page
    result["code"]=0
    result["msg"]="显示成功"
    return_data = c.get_classes(start_index,end_index,per_page)
    result["data"] = return_data["classes"]
    result["total_pages"] = return_data["total_pages"]
    result["class_num"] = return_data["class_num"]
    return jsonify(result)

def Admin_showclassstudents(class_id,page,per_page):
    # 管理员查看某班学生名单业务接口封装
    result = {}
    s = Student_Operation()
    start_index = (page - 1) * per_page
    end_index = page * per_page
    result["code"]=0
    result["msg"]="显示成功"
    return_data = s.get_students_by_class(class_id,start_index,end_index,per_page)
    result["data"] = return_data["students"]
    result["total_pages"] = return_data["total_pages"]
    result["student_num"] = return_data["student_num"]
    return jsonify(result)

def Admin_showallstudents(page,per_page):
    # 管理员查看所有学生名单业务接口封装
    result = {}
    s = Student_Operation()
    start_index = (page - 1) * per_page
    end_index = page * per_page
    result["code"] = 0
    result["msg"]="显示成功"
    return_data = s.get_all_students(start_index,end_index,per_page)
    result["data"] = return_data["students"]
    result["total_pages"] = return_data["total_pages"]
    result["student_num"] = return_data["student_num"]
    return jsonify(result)

def Admin_createstudent(student_id, class_id, name, gender):
    # 管理员创建学生信息业务接口封装
    result = {}
    s = Student_Operation()
    student_data = s.find_student_by_id(student_id)
    c = Class_Operation()
    cms_class = c.find_class_by_id(class_id)
    if cms_class is not None:
        if student_data is None:
            result['code'] = 0
            result['msg'] = "创建成功"
            s.create_student(student_id, class_id, name, gender)
        else:
            result['code'] = 1
            result['msg'] = "创建失败，学号已存在"
    else:
        result['code'] = 2
        result['msg'] = "创建失败，班级号不存在"
    return result

def Admin_deletestudent(student_id):
    # 管理员删除学生信息业务接口封装
    result = {}
    s = Student_Operation()
    student_data = s.find_student_by_id(student_id)
    # 输入学号不存在时删除失败，存在时执行删除操作
    if student_data is None:
        result['code'] = 1
        result['msg'] = "删除失败，学号不存在"
    else:
        result['code'] = 0
        result['msg'] = "删除成功"
        s.delete_student(student_id)
    return result

def Admin_showexceptions(page,per_page):
    # 管理员查看所有异常帧记录接口封装
    result = {}
    e= Exception_Operation()
    start_index = (page - 1) * per_page
    end_index = page * per_page
    result["code"]=0
    result["msg"]="显示成功"
    return_data = e.get_exceptions(start_index,end_index,per_page)
    result["data"] = return_data["exceptions"]
    result["total_pages"] = return_data["total_pages"]
    return jsonify(result)

def Admin_deleteexception(id):
    # 管理员删除异常帧记录接口封装
    result = {}
    e = Exception_Operation()
    exception = e.find_exception_by_id(id)
    if exception is None:
        result['code'] = 1
        result['msg'] = "删除失败，记录不存在"
    else:
        result['code'] = 0
        result['msg'] = "删除成功"
        e.delete_exception(id)
    return result

def Admin_showstatistics():
    # 管理员查看统计信息接口封装
    result = {}
    u = User_Operation()
    c = Class_Operation()
    e = Exception_Operation()
    b = Browse_Operation()
    s = Student_Operation()
    result['teacher_num'] = u.count_teacher_num()
    result['class_num'] = c.count_class_num()
    result['student_num'] = s.count_student_num()
    result['exception_num_past_week'] = e.count_exception_num_past_week()
    result['browse_num_past_week'] = b.count_browse_num_past_week()
    result['exception_data'] = e.count_exceptions_for_previous_days()
    result['exception_constitution'] = e.calculate_tag_num()
    result['browse_data'] = b.count_browse_for_previous_days()
    return jsonify(result)

