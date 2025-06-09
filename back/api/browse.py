from operation.browse import Browse_Operation

def Browse_record(teacher_account,time,class_id):
    result = {}
    b = Browse_Operation()
    data = b.record(teacher_account=teacher_account, time=time, class_id=class_id)
    if not data:
        result["code"] = 0
        result['msg'] = "浏览记录成功"
    else:
        result['code'] = 1
        result['msg'] = "浏览记录失败"

    return result


