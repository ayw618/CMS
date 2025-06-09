import requests
import cv2
import json
import sys
from main_window import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QComboBox, QMainWindow, QPushButton, QLabel, QVBoxLayout, \
    QWidget, QDesktopWidget
from PyQt5.QtGui import QColor, QRegExpValidator, QImage, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QRegExp, QUrl, Qt, QTimer
from functools import partial
from datetime import datetime

class startShow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(startShow, self).__init__(parent=None)  # 初始化父类
        self.setupUi(self)  # 使用Ui_MainWindow的设置初始化窗口UI
        self.main_stackedWidget.setCurrentWidget(self.page1)  # 设置QStackedWidget当前显示的页面为page1
        self.url = 'http://10.203.235.77:5000'  # 设置URL
        self.warning.hide()  # 隐藏警告控件
        self.teacher_warning1.hide()  # 隐藏班主任警告1
        self.teacher_warning2.hide()  # 隐藏班主任警告2
        self.teacher_success.hide()  # 隐藏班主任成功提示
        self.teacher_check_password_edit.hide()  # 隐藏班主任密码检查编辑框
        self.teacher_old_password_edit.hide()  # 隐藏班主任旧密码编辑框
        self.teacher_new_password_edit.hide()  # 隐藏班主任新密码编辑框
        self.teacher_check_pushbutton.hide()  # 隐藏班主任密码检查按钮
        self.teacher_change_pushbutton.show()  # 显示班主任密码更改按钮
        self.boss_warning1.hide()  # 隐藏教导主任警告1
        self.boss_warning2.hide()  # 隐藏教导主任警告2
        self.boss_success.hide()  # 隐藏教导主任成功提示
        self.boss_check_password_edit.hide()  # 隐藏教导主任密码检查编辑框
        self.boss_old_password_edit.hide()  # 隐藏教导主任旧密码编辑框
        self.boss_new_password_edit.hide()  # 隐藏教导主任新密码编辑框
        self.boss_check_pushbutton.hide()  # 隐藏教导主任密码检查按钮
        self.boss_change_pushbutton.show()  # 显示教导主任密码更改按钮
        # 记录账号, 班级
        self.current_account = {}
        self.class_id = {}
        # start页面的登录按钮
        self.startPushButton.clicked.connect(self.show_page2)
        # login界面返回按钮
        self.back_pushbutton.clicked.connect(self.show_page1)
        # 在此只能输入数字 登录页面
        self.userAccountEdit.setValidator(QRegExpValidator(QRegExp("[0-9]+$")))
        # 在此只能输入数字和字母 登录页面
        self.passwordEdit.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9]+$")))
        # 在此只能输入数字和字母 教导主任改密码
        self.boss_new_password_edit.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9]+$")))
        self.boss_old_password_edit.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9]+$")))
        self.boss_check_password_edit.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9]+$")))
        # 在此只能输入数字和字母  班主任改密码
        self.teacher_new_password_edit.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9]+$")))
        self.teacher_old_password_edit.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9]+$")))
        self.teacher_check_password_edit.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9]+$")))

        # 登录界面的登录按键
        self.loginPushButton.clicked.connect(self.click_loginPushButton)
        # 显示界面的listWidget
        self.teacher_listWidget.itemClicked.connect(self.teacher_switch_page)
        self.boss_listWidget.itemClicked.connect(self.boss_switch_page)
        # 显示界面的按钮操作
        self.teacher_change_pushbutton.clicked.connect(self.click_teacher_changePushButton)
        self.teacher_check_pushbutton.clicked.connect(self.click_teacher_checkPushButton)
        self.boss_change_pushbutton.clicked.connect(self.click_boss_changePushButton)
        self.boss_check_pushbutton.clicked.connect(self.click_boss_checkPushButton)
        # 实现可拖动窗口
        self.start_x = None
        self.start_y = None
        self.anim = None
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 设置窗口标志：隐藏窗口边框

        # 实现读取视频
        # 创建一个标签用于显示视频帧
        self.image_label = QLabel(self)  # 创建标签控件
        self.image_label.setAlignment(Qt.AlignCenter)  # 设置标签内容居中显示
        self.image_label1 = QLabel(self)  # 创建标签控件
        self.image_label1.setAlignment(Qt.AlignCenter)  # 设置标签内容居中显示
        self.central_layout = QVBoxLayout()
        self.central_layout.addWidget(self.image_label)
        self.central_layout1 = QVBoxLayout()
        self.central_layout1.addWidget(self.image_label1)
        self.teacher_video_pushbutton.clicked.connect(self.teacher_start_video)
        self.teacher_close_pushbutton.clicked.connect(self.teacher_close_video)
        self.boss_video_pushbutton.clicked.connect(self.boss_start_video)
        self.boss_close_pushbutton.clicked.connect(self.boss_close_video)
        self.html_next_pushbutton.clicked.connect(self.html_change_next)
        self.html_last_pushbutton.clicked.connect(self.html_change_last)

    def teacher_start_video(self):
        browser_data = {
            'teacher_account': self.current_account['user_account'],
            'time': str(datetime.now()),
            'class_id': self.class_id['class_id'],
        }
        json_data = json.dumps(browser_data)
        browser_url = self.url + "/teacher/recordbrowse"
        headers = {
            "Content-Type": "application/json"
        }
        requests.post(browser_url, data=json_data, headers=headers)
        self.teacher_video_widget.setLayout(self.central_layout)
        self.timer = QTimer(self)  # 创建定时器
        self.timer.timeout.connect(self.teacher_update_video_frame)  # 将定时器的超时信号连接到 update_video_frame 槽函数
        self.video_capture = None
        video_url = self.url + '/teacher/monitor?class_id=' + self.class_id['class_id']
        self.video_capture = cv2.VideoCapture(video_url)  # 使用 OpenCV 打开视频流
        self.timer.start(30)  # 启动定时器，设置更新频率为30毫秒
        self.teacher_video_pushbutton.hide()
        self.teacher_close_pushbutton.show()

    def teacher_update_video_frame(self):
        if self.video_capture is not None:
            ret, frame = self.video_capture.read()  # 从视频流中读取帧
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 转换颜色通道为 RGB 顺序
            if ret:
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                self.image_label.setPixmap(pixmap)  # 在标签中显示图像

    def teacher_close_video(self):
        if self.video_capture is not None:
            self.timer.stop()
            self.video_capture.release()
            self.image_label.setPixmap(QPixmap(""))  # 在标签中显示图像
            self.teacher_video_pushbutton.show()
            self.teacher_close_pushbutton.hide()

    def boss_start_video(self):
        # 1,2,3对应a,b,c班级
        if str(self.boss_choose_class_lineedit.text()) == '1':
            browser_data = {
                'teacher_account': self.current_account['user_account'],
                'time': str(datetime.now()),
                'class_id': 'a',
            }
            json_data = json.dumps(browser_data)
            browser_url = self.url + "/teacher/recordbrowse"
            headers = {
                "Content-Type": "application/json"
            }
            requests.post(browser_url, data=json_data, headers=headers)
            self.class_warning.hide()
            self.noclass_warning.hide()
            self.boss_video_widget.setLayout(self.central_layout1)
            self.timer = QTimer(self)  # 创建定时器
            self.timer.timeout.connect(self.boss_update_video_frame)  # 将定时器的超时信号连接到 update_video_frame 槽函数
            self.video_capture = None
            video_url = self.url + '/teacher/monitor?class_id=a'
            self.video_capture = cv2.VideoCapture(video_url)  # 使用 OpenCV 打开视频流
            self.timer.start(30)  # 启动定时器，设置更新频率为30毫秒
            self.boss_video_pushbutton.hide()
            self.boss_close_pushbutton.show()
        elif str(self.boss_choose_class_lineedit.text()) == '2':
            browser_data = {
                'teacher_account': self.current_account['user_account'],
                'time': str(datetime.now()),
                'class_id': 'b',
            }
            json_data = json.dumps(browser_data)
            browser_url = self.url + "/teacher/recordbrowse"
            headers = {
                "Content-Type": "application/json"
            }
            requests.post(browser_url, data=json_data, headers=headers)
            self.class_warning.hide()
            self.noclass_warning.hide()
            self.boss_video_widget.setLayout(self.central_layout1)
            self.timer = QTimer(self)  # 创建定时器
            self.timer.timeout.connect(self.boss_update_video_frame)  # 将定时器的超时信号连接到 update_video_frame 槽函数
            self.video_capture = None
            video_url = self.url + '/teacher/monitor?class_id=b'
            self.video_capture = cv2.VideoCapture(video_url)  # 使用 OpenCV 打开视频流
            self.timer.start(30)  # 启动定时器，设置更新频率为30毫秒
            self.boss_video_pushbutton.hide()
            self.boss_close_pushbutton.show()
        elif str(self.boss_choose_class_lineedit.text()) == '3':
            browser_data = {
                'teacher_account': self.current_account['user_account'],
                'time': str(datetime.now()),
                'class_id': 'c',
            }
            json_data = json.dumps(browser_data)
            browser_url = self.url + "/teacher/recordbrowse"
            headers = {
                "Content-Type": "application/json"
            }
            requests.post(browser_url, data=json_data, headers=headers)
            self.class_warning.hide()
            self.noclass_warning.hide()
            self.boss_video_widget.setLayout(self.central_layout1)
            self.timer = QTimer(self)  # 创建定时器
            self.timer.timeout.connect(self.boss_update_video_frame)  # 将定时器的超时信号连接到 update_video_frame 槽函数
            self.video_capture = None
            video_url = self.url + '/teacher/monitor?class_id=c'
            self.video_capture = cv2.VideoCapture(video_url)  # 使用 OpenCV 打开视频流
            self.timer.start(30)  # 启动定时器，设置更新频率为30毫秒
            self.boss_video_pushbutton.hide()
            self.boss_close_pushbutton.show()
        elif str(self.boss_choose_class_lineedit.text()) == '':
            self.noclass_warning.show()
            self.class_warning.hide()
        else:
            self.class_warning.show()
            self.noclass_warning.hide()

    def boss_update_video_frame(self):
        if self.video_capture is not None:
            ret, frame = self.video_capture.read()  # 从视频流中读取帧
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 转换颜色通道为 RGB 顺序
            if ret:
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                self.image_label1.setPixmap(pixmap)  # 在标签中显示图像

    def boss_close_video(self):
        if self.video_capture is not None:
            self.timer.stop()
            self.video_capture.release()
            self.image_label1.setPixmap(QPixmap(""))  # 在标签中显示图像
            self.boss_video_pushbutton.show()
            self.boss_close_pushbutton.hide()
            self.boss_choose_class_lineedit.clear()

    # 以下四个函数为实现页面可拖动重写的函数
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            super(startShow, self).mousePressEvent(event)
            self.start_x = event.x()
            self.start_y = event.y()

    def mouseReleaseEvent(self, event):
        self.start_x = None
        self.start_y = None

    def mouseMoveEvent(self, event):
        try:
            super(startShow, self).mouseMoveEvent(event)
            dis_x = event.x() - self.start_x
            dis_y = event.y() - self.start_y
            self.move(self.x() + dis_x, self.y() + dis_y)
        except:
            pass

    def effect_shadow_style(self, widget):
        effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        effect_shadow.setOffset(12, 12)  # 偏移
        effect_shadow.setBlurRadius(128)  # 阴影半径
        effect_shadow.setColor(QColor(155, 230, 237, 150))  # 阴影颜色
        widget.setGraphicsEffect(effect_shadow)

    # 当点击班主任密码更改按钮时触发的槽函数
    def click_teacher_changePushButton(self):
        # 显示班主任密码检查按钮和编辑框
        self.teacher_check_pushbutton.show()
        self.teacher_old_password_edit.show()
        self.teacher_new_password_edit.show()
        self.teacher_check_password_edit.show()
        self.teacher_check_pushbutton.show()
        # 隐藏班主任密码更改按钮
        self.teacher_change_pushbutton.hide()

    # 当点击班主任密码检查按钮时触发的槽函数
    def click_teacher_checkPushButton(self):
        # 从编辑框中获取班主任密码相关数据
        qt_data = {
            'user_account': self.current_account['user_account'],
            'OldPassword': str(self.teacher_old_password_edit.text()),
            'NewPassword': str(self.teacher_new_password_edit.text()),
            'RecheckedPassword': str(self.teacher_check_password_edit.text()),
        }
        # 将数据转换为 JSON 格式
        json_data = json.dumps(qt_data)
        url = self.url + "/teacher/ChangePassword"  # 设置请求的URL
        headers = {
            "Content-Type": "application/json"
        }
        # 发送 POST 请求，获取后端返回的数据并转换为 JSON 格式
        back_end_data = (requests.post(url, data=json_data, headers=headers)).json()

        # 根据后端返回的代码显示不同的警告或成功消息
        if back_end_data['code'] == 0:
            self.teacher_warning1.hide()
            self.teacher_warning2.hide()
            self.teacher_success.show()
        elif back_end_data['code'] == 1:
            self.teacher_warning1.show()
            self.teacher_warning2.hide()
            self.teacher_success.hide()
        elif back_end_data['code'] == 2:
            self.teacher_warning1.hide()
            self.teacher_warning2.show()
            self.teacher_success.hide()

    # 当点击教导主任密码更改按钮时触发的槽函数
    def click_boss_changePushButton(self):
        # 显示教导主任密码检查按钮和编辑框
        self.boss_check_pushbutton.show()
        self.boss_old_password_edit.show()
        self.boss_new_password_edit.show()
        self.boss_check_password_edit.show()
        self.boss_check_pushbutton.show()
        # 隐藏教导主任密码更改按钮
        self.boss_change_pushbutton.hide()

    # 当点击教导主任密码检查按钮时触发的槽函数
    def click_boss_checkPushButton(self):
        # 从编辑框中获取教导主任密码相关数据
        qt_data = {
            'user_account': self.current_account['user_account'],
            'OldPassword': str(self.boss_old_password_edit.text()),
            'NewPassword': str(self.boss_new_password_edit.text()),
            'RecheckedPassword': str(self.boss_check_password_edit.text()),
        }
        # 将数据转换为 JSON 格式
        json_data = json.dumps(qt_data)
        url = self.url + "/teacher/ChangePassword"  # 设置请求的URL，可能需要修改为教导主任密码更改的URL
        headers = {
            "Content-Type": "application/json"
        }
        # 发送 POST 请求，获取后端返回的数据并转换为 JSON 格式
        back_end_data = (requests.post(url, data=json_data, headers=headers)).json()

        # 根据后端返回的代码显示不同的警告或成功消息
        if back_end_data['code'] == 0:
            self.boss_warning1.hide()
            self.boss_warning2.hide()
            self.boss_success.show()
        elif back_end_data['code'] == 1:
            self.boss_warning1.show()
            self.boss_warning2.hide()
            self.boss_success.hide()
        elif back_end_data['code'] == 2:
            self.boss_warning1.hide()
            self.boss_warning2.show()
            self.boss_success.hide()

    def show_page1(self):
        self.main_stackedWidget.setCurrentWidget(self.page1)

    def show_page2(self):
        self.main_stackedWidget.setCurrentWidget(self.page2)

    def show_page3(self):
        self.main_stackedWidget.setCurrentWidget(self.page3)

    def show_page4(self):
        self.main_stackedWidget.setCurrentWidget(self.page4)

    def show_teacher_page1(self):
        self.teacher_stackedWidget.setCurrentWidget(self.page3_1)

    def show_teacher_page2(self):
        self.teacher_stackedWidget.setCurrentWidget(self.page3_2)

    def show_teacher_page3(self):
        self.teacher_stackedWidget.setCurrentWidget(self.page3_3)

    def show_boss_page1(self):
        self.teacher_stackedWidget.setCurrentWidget(self.page4_1)

    def show_boss_page2(self):
        self.teacher_stackedWidget.setCurrentWidget(self.page4_2)

    def show_boss_page3(self):
        self.teacher_stackedWidget.setCurrentWidget(self.page4_3)

    def show_boss_page4(self):
        self.teacher_stackedWidget.setCurrentWidget(self.page4_4)

    # 处理班主任页面切换的槽函数，根据不同的列表项切换到不同的页面
    def teacher_switch_page(self, item):
        if item == self.teacher_listWidget.item(0):
            # 切换到第一个页面（page3_1）
            self.teacher_stackedWidget.setCurrentWidget(self.page3_1)
            self.teacher_video_pushbutton.show()
            self.teacher_close_pushbutton.hide()
            # 清空密码编辑框
            self.teacher_old_password_edit.clear()
            self.teacher_check_password_edit.clear()
            self.teacher_new_password_edit.clear()
        elif item == self.teacher_listWidget.item(1):
            # 切换到第二个页面（page3_2）
            self.teacher_stackedWidget.setCurrentWidget(self.page3_2)
            if self.class_id['class_id'] == "a":
                number = 1
                self.scrollArea_a.show()
                self.scrollArea_b.hide()
                self.scrollArea_c.hide()
            elif self.class_id['class_id'] == "b":
                number = 2
                self.scrollArea_a.hide()
                self.scrollArea_b.show()
                self.scrollArea_c.hide()
            else:
                number = 3
                self.scrollArea_a.hide()
                self.scrollArea_b.hide()
                self.scrollArea_c.show()
            self.page3_2_lineEdit.setText(str(number) + '班')
            # 清空密码编辑框
            self.teacher_old_password_edit.clear()
            self.teacher_check_password_edit.clear()
            self.teacher_new_password_edit.clear()
        elif item == self.teacher_listWidget.item(2):
            # 切换到第三个页面（page3_3）
            self.teacher_stackedWidget.setCurrentWidget(self.page3_3)
            self.teacher_warning1.hide()
            self.teacher_warning2.hide()
            self.teacher_success.hide()
            self.teacher_check_password_edit.hide()
            self.teacher_old_password_edit.hide()
            self.teacher_new_password_edit.hide()
            self.teacher_check_pushbutton.hide()
            self.teacher_change_pushbutton.show()
        elif item == self.teacher_listWidget.item(3):
            # 切换回主页面（page2）
            self.main_stackedWidget.setCurrentWidget(self.page2)
            # 清空编辑框
            self.teacher_old_password_edit.clear()
            self.teacher_check_password_edit.clear()
            self.teacher_new_password_edit.clear()
            self.teacher_name_edit.clear()
            self.teacher_role_edit.clear()
            self.teacher_account_edit.clear()
            # 登出返回状态
            json_account = json.dumps(self.current_account)
            url_logout = self.url + "/teacher/Logout"
            headers = {
                "Content-Type": "application/json",
            }
            requests.post(url_logout, data=json_account, headers=headers)

    # 处理班主任页面切换的槽函数，根据不同的列表项切换到不同的页面
    def boss_switch_page(self, item):
        if item == self.boss_listWidget.item(0):
            # 切换到第一个页面（page4_1）
            self.boss_stackedWidget.setCurrentWidget(self.page4_1)
            self.class_warning.hide()
            self.noclass_warning.hide()
            self.boss_video_pushbutton.show()
            self.boss_close_pushbutton.hide()
            # 清空密码编辑框和账号编辑框
            self.boss_old_password_edit.clear()
            self.boss_check_password_edit.clear()
            self.boss_new_password_edit.clear()
            self.passwordEdit.clear()
        elif item == self.boss_listWidget.item(1):
            # 切换到第二个页面（page4_2）
            self.boss_old_password_edit.clear()
            self.boss_check_password_edit.clear()
            self.boss_new_password_edit.clear()
            self.boss_stackedWidget.setCurrentWidget(self.page4_2)

            self.html_stackedWidget.setCurrentWidget(self.html_page1)
            self.html_next_pushbutton.show()
            self.html_last_pushbutton.hide()
            # 创建 QWebEngineView 并加载外部 web 界面
            self.browser1 = QWebEngineView(self.html_widget1)
            self.browser1.setGeometry(0, 0, 760, 480)
            self.browser1.load(QUrl(self.url + '/teacher/statistics'))
            self.browser1.show()

        elif item == self.boss_listWidget.item(2):
            # 切换到第三个页面（page4_3）
            self.boss_stackedWidget.setCurrentWidget(self.page4_3)
            self.boss_warning1.hide()
            self.boss_warning2.hide()
            self.boss_success.hide()
            self.boss_check_password_edit.hide()
            self.boss_old_password_edit.hide()
            self.boss_new_password_edit.hide()
            self.boss_check_pushbutton.hide()
            self.boss_change_pushbutton.show()
        elif item == self.boss_listWidget.item(3):
            # 切换回主页面（page2）
            self.boss_old_password_edit.clear()
            self.boss_check_password_edit.clear()
            self.boss_new_password_edit.clear()
            self.boss_name_edit.clear()
            self.boss_role_edit.clear()
            self.boss_account_edit.clear()
            self.main_stackedWidget.setCurrentWidget(self.page2)
            # 登出返回状态
            json_account = json.dumps(self.current_account)
            url = self.url + "/teacher/Logout"
            headers = {
                "Content-Type": "application/json",
            }
            requests.post(url, data=json_account, headers=headers)

    def html_change_next(self):
        self.html_stackedWidget.setCurrentWidget(self.html_page2)
        self.html_next_pushbutton.hide()
        self.html_last_pushbutton.show()
        # 创建 QWebEngineView 并加载外部 web 界面
        self.browser2 = QWebEngineView(self.html_widget2)
        self.browser2.setGeometry(0, 0, 760, 420)
        self.browser2.load(QUrl(self.url + '/teacher/tagstatistics'))
        self.browser2.show()

    def html_change_last(self):
        self.html_stackedWidget.setCurrentWidget(self.html_page1)
        self.html_next_pushbutton.show()
        self.html_last_pushbutton.hide()
        # 创建 QWebEngineView 并加载外部 web 界面
        self.browser1 = QWebEngineView(self.html_widget1)
        self.browser1.setGeometry(0, 0, 760, 480)
        self.browser1.load(QUrl(self.url + '/teacher/statistics'))
        self.browser1.show()

    # 读取登录界面的编辑框内容并返回一个包含用户账号和密码的字典
    def readloginEdit(self):
        return {
            'user_account': str(self.userAccountEdit.text()),
            'password': str(self.passwordEdit.text()),
        }

    # 处理登录按钮点击事件
    def click_loginPushButton(self):
        qt_data = self.readloginEdit()  # 读取编辑框内容
        json_data = json.dumps(qt_data)  # 将数据转换为 JSON 格式
        url = self.url + "/teacher/Login"  # 构建请求的 URL
        headers = {
            "Content-Type": "application/json"
        }
        back_end_data = (requests.post(url, data=json_data, headers=headers)).json()  # 发送 POST 请求并获取后端返回的数据

        if back_end_data['code'] == 0:
            # 登录成功，切换到班主任页面
            self.warning.hide()
            self.class_id = {'class_id': str(back_end_data['class_id']['class_id'])}
            self.current_account = {'user_account': str(self.userAccountEdit.text()), }
            self.main_stackedWidget.setCurrentWidget(self.page3)
            self.teacher_stackedWidget.setCurrentWidget(self.page3_4)
            self.teacher_listWidget.clearSelection()
            self.userAccountEdit.clear()
            self.passwordEdit.clear()
            self.teacher_name_edit.setText(str(back_end_data['user']['name']))
            self.teacher_role_edit.setText('班主任')
            self.teacher_account_edit.setText(str(back_end_data['user']['user_account']))
        elif back_end_data['code'] == 10:
            # 登录成功，切换到教导主任页面
            self.warning.hide()
            self.current_account = {'user_account': str(self.userAccountEdit.text()), }
            self.main_stackedWidget.setCurrentWidget(self.page4)
            self.boss_stackedWidget.setCurrentWidget(self.page4_4)
            self.boss_listWidget.clearSelection()
            self.userAccountEdit.clear()
            self.passwordEdit.clear()
            self.boss_name_edit.setText(str(back_end_data['user']['name']))
            self.boss_role_edit.setText('教导主任')
            self.boss_account_edit.setText(str(back_end_data['user']['user_account']))
        else:
            # 登录失败，显示警告
            self.warning.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    start = startShow()
    start.show()
    sys.exit(app.exec_())  # 修正此行，调用 app.exec_()
