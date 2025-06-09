from ultralytics import YOLO
import cv2
import os

path_name = os.getcwd()

class Image_Analysis():
    def __init__(self,class_id):
        # 打开视频文件
        self.class_id = class_id
        self.video = cv2.VideoCapture(path_name + '/ai/' + 'video_' + class_id + '.MP4')

        # 加载yolo模型
        model_path = path_name + '/ai/best.pt'
        self.model = YOLO(model_path)

    def __del__(self):
        self.video.release()

    def get_frame(self,class_id):
        success, image = self.video.read()

        if not success:
            self.video = cv2.VideoCapture(path_name + '/ai/' + 'video_' + class_id + '.MP4')
            return None, None  # 如果没有成功读取帧，返回空的帧和类别信息列表
        results = self.model(image)

        annotated_frame = results[0].plot()  # 画框

        # 获取检测到的对象的类别信息列表
        class_values = results[0].boxes.cls.tolist()

        return annotated_frame, class_values