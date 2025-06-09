import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QComboBox,QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
import requests

# 创建 PyQt5 应用程序
class VideoStreamApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Stream Viewer")  # 设置窗口标题
        self.setGeometry(100, 100, 800, 600)  # 设置窗口位置和大小


        self.url_combo = QComboBox(self)
        self.url_combo.addItem("a")
        self.url_combo.addItem("b")
        self.url_combo.addItem("c")
        self.url_combo.currentIndexChanged.connect(self.update_selected_url)

        # 创建一个按钮，点击后开始播放视频
        self.start_button = QPushButton("Start Video")
        self.start_button.clicked.connect(self.start_video)  # 连接按钮的点击事件到 start_video 方法

        # 创建一个标签用于显示视频帧
        self.image_label = QLabel(self)  # 创建标签控件
        self.image_label.setAlignment(Qt.AlignCenter)  # 设置标签内容居中显示

        control_widget = QWidget()
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.url_combo)
        control_layout.addWidget(self.start_button)
        control_widget.setLayout(control_layout)

        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.image_label)
        central_layout.addWidget(control_widget, alignment=Qt.AlignBottom | Qt.AlignRight)  # Align to right bottom
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        self.timer = QTimer(self)  # 创建定时器
        self.timer.timeout.connect(self.update_video_frame)  # 将定时器的超时信号连接到 update_video_frame 槽函数

        self.video_capture = None
        self.selected_url = 'a'

    def update_selected_url(self):
        # Update the selected URL based on the combo box selection
        self.selected_url = self.url_combo.currentText()

    def start_video(self):
        try:
            if self.selected_url == "a":
                video_url = 'http://127.0.0.1:5000/teacher/monitor?class_id=a'
            elif self.selected_url == "b":
                video_url = 'http://127.0.0.1:5000/teacher/monitor?class_id=b'
            elif self.selected_url == "c":
                video_url = 'http://127.0.0.1:5000/teacher/monitor?class_id=c'
            else:
                video_url = 'http://127.0.0.1:5000/teacher/monitor?class_id=a'
            self.video_capture = cv2.VideoCapture(video_url)  # 使用 OpenCV 打开视频流
            self.timer.start(40)  # 启动定时器，设置更新频率为30毫秒
        except Exception as e:
            print("Error:", e)  # 捕获并打印任何异常错误信息

    def update_video_frame(self):
        if self.video_capture is not None:
            ret, frame = self.video_capture.read()  # 从视频流中读取帧
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 转换颜色通道为 RGB 顺序
            if ret:
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                self.image_label.setPixmap(pixmap)  # 在标签中显示图像

# 主函数，创建 PyQt5 应用程序对象并运行
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoStreamApp()  # 创建主窗口对象
    window.show()  # 显示主窗口
    sys.exit(app.exec_())  # 运行应用程序事件循环并等待退出信号