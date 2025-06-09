from ai.image_analysis import Image_Analysis
import datetime
import os,cv2
import time
from operation.exception import Exception_Operation


path_name = os.getcwd()

def Teacher_monitor(class_id):
    ai_analysis = Image_Analysis(class_id=class_id)
    last_record_time = datetime.datetime.now()  # 记录上一次异常的时间

    while True:
        annotated_frame, class_values = ai_analysis.get_frame(class_id=class_id)

        if annotated_frame is None:
            print('frame is None')
            continue

        if class_values: # 有异常情况
            current_time = datetime.datetime.now()

            if (current_time - last_record_time).total_seconds() >= 0.7:# 检查是否距离上次记录已经过去0.7秒
                time = current_time.strftime('%Y-%m-%d %H:%M:%S')

                # 保存图像到一个可访问的位置
                filename = time.replace(' ', '__').replace('-','_').replace(':','_')+'__'+class_id+'.jpg'


                cv2.imwrite(path_name +'/static/' +filename, annotated_frame)

                # 返回图像URL，记得修改成相应的地址！！！
                # url = 'http://10.203.132.217:5000/static/'+ filename
                url = '/static/' + filename
                time = current_time.strftime('%Y-%m-%d %H:%M:%S')
                # 记录异常情况
                e = Exception_Operation()
                e.record(time=time, class_id=class_id, class_values=class_values, link=url)
                last_record_time = current_time

        ret, buffer = cv2.imencode('.jpg', annotated_frame)  # 编码为 jpg 格式
        frame_byte = buffer.tobytes()  # 转换为 bytes 类型

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_byte + b'\r\n')

def Teacher_score():
    e = Exception_Operation()
    result = {}
    data=e.calculate_and_store_scores()
    if data==0:
        result["code"] = 0
        result['msg'] = "积分成功"
    else:
        result['code'] = 1
        result['msg'] = "积分失败"

    return result


def Teacher_statistics():
    e = Exception_Operation()
    data = e.statistics_for_chart()

    return data

def Teacher_tagstatistics():
    e = Exception_Operation()
    data = e.tag_statistics()
    # e.change_link()

    return data










