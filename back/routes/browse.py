#routes\browse.py


from flask import Blueprint,request
import json
from api.browse import *

# 第1步
browse = Blueprint('browse', __name__)

@browse.route('/recordbrowse', methods=['POST'])
def recordbrowse():
    data = json.loads(request.data)
    teacher_account = data['teacher_account']
    time = data['time']
    class_id = data['class_id']
    result=Browse_record(teacher_account=teacher_account,time=time,class_id=class_id)
    return result













