from flask import Blueprint,request,Response,render_template
import json
# 第1步
teacher = Blueprint('teacher', __name__)

from api.teacher import *
from api.exception import *

#注册教师账户
@teacher.route('/register', methods=['POST'])
def register():
    data = json.loads(request.data)
    user_account = data['user_account']
    password = data['password']
    name = data['name']
    role = data['role']
    state = data['state']

    result = Teacher_register(user_account=user_account, password=password, name=name,role= role, state=state)
    return result

#删除教师账户
@teacher.route('/deregister',methods=['POST'])
def deluser():
    data=json.loads(request.data)
    user_account = data['user_account']
    result = Teacher_delete(user_account = user_account)
    return result

#修改教师密码
@teacher.route('/ChangePassword', methods=['POST'])
def ChangePassword():
    data = json.loads(request.data)
    user_account = data['user_account']
    OldPassword = data['OldPassword']
    NewPassword = data['NewPassword']
    RecheckedPassword = data['RecheckedPassword']

    result =Teacher_ChangePassword(user_account=user_account, oldpassword=OldPassword,newpassword=NewPassword,recheckedpassword=RecheckedPassword)
    return result

@teacher.route('/Login',methods=['post'])
def Login():
    data = json.loads(request.data)
    user_account = data['user_account']
    password = data['password']

    result = Teacher_login(user_account=user_account, password=password)
    return result

@teacher.route('/Logout',methods=['post'])
def Logout():
    data = json.loads(request.data)
    user_account = data['user_account']
    result = Teacher_logout(user_account=user_account)
    return result


@teacher.route('/monitor', methods=['GET'])
def monitor():
    # data = json.loads(request.data)
    class_id = request.args.get('class_id')
    result = Teacher_monitor(class_id=class_id)

    if result is None:
        return Response("No data", mimetype='text/plain')

    return Response(result, mimetype='multipart/x-mixed-replace; boundary=frame')


@teacher.route('/score', methods=['POST'])
def score():
    # data = json.loads(request.data)
    result = Teacher_score()
    return result

@teacher.route('/statistics')
def statistics():
    data = Teacher_statistics()
    print(data)
    if  data:
        # 解析字典获取参数，如果不存在，则使用默认值
        received_classIds = data.get('classIds', ["ClassA", "ClassB", "ClassC", "ClassE"])
        received_dates = data.get('dates', ["2023-09-01", "2023-09-02", "2023-09-03", "2023-09-04"])
        received_scores = data.get('scores', [
            [70, 70, 70, 70],
            [80, 80, 80, 80],
            [90, 90, 90, 90],
            [100, 100, 100, 100]
        ])
        # 将数据传递给HTML模板
        return render_template('chart.html', classIds=received_classIds, dates=received_dates, scores=received_scores)
    else:
        return data

@teacher.route('/tagstatistics')
def tagstatistics():
    data = Teacher_tagstatistics()
    received_data = {
        "bow_head": data.get('bow_head', []),
        "chatting": data.get('chatting', []),
        "eating": data.get('eating', []),
        "enter_exit": data.get('enter_exit', []),
        "play_phone": data.get('play_phone', []),
    }
    return render_template('barchart.html', data=received_data)













