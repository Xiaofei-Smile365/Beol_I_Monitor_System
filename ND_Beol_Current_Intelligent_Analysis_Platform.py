# -*- coding: utf-8 -*-
"""
@Time    : 2020/6/23 19:48
@Author  : Xiaofei
@Contact : smile.qiangqian@Gmail.com
@File    : ND_Beol_Current_Intelligent_Analysis_Platform.py
@Version : 1.0
@IDE     : PyCharm
@Source  : python -m pip install *** -i https://pypi.tuna.tsinghua.edu.cn/simple
"""
import sys  # 载入必需的模块
import os

import datetime

from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap, QFont
from PyQt5.QtCore import Qt

from real_time_data_monitor import Real_time_data_monitor

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']  # Prevent packaging errors on windows system
from PyQt5 import QtCore
from PyQt5.QtWidgets import *  # 在Qt5中使用的基本的GUI窗口控件都在PyQt5.QtWidgets模块中

from data_log_analysis import data_log_analysis
from ftplib import FTP


class MainWindow(QWidget):
    def __init__(self, parent=None):  # 基础窗口控件QWidget类是所有用户界面对象的基类， 所有的窗口和控件都直接或间接继承自QWidget类。
        super(MainWindow, self).__init__(parent)  # 使用super函数初始化窗口

        self.setWindowTitle('ND Beol 电流智能分析平台')  # 设定窗口控件的标题
        self.setWindowIcon(QIcon('./plotform.ico'))  # 设定窗口的图标
        self.resize(1366, 768)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap('./background.png').scaled(self.width(), self.height())))  # 设定UI界面背景图片
        self.setPalette(palette)
        self.setFixedSize(1366, 768)

        self.layout_set()

        self.the_real_time_data_monitor_window = Real_time_data_monitor()

    def layout_set(self):
        self.label_title = QLabel(self)
        self.label_title.setText('<b>ND Beol 电流智能分析平台<b>')
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet('color: #3a74e2')
        self.label_title.setFont(QFont('微软雅黑', 24))
        self.label_title.setFixedSize(700, 40)
        self.h_box_title = QHBoxLayout()
        self.h_box_title.addWidget(self.label_title)

        self.h_box_auo_logo_title_time_logo = QHBoxLayout()
        self.h_box_auo_logo_title_time_logo.addLayout(self.h_box_title)

        self.label_owner = QLabel(self)
        self.label_owner.setText('<b>AUO MS06H3<b>')
        self.label_owner.setAlignment(Qt.AlignLeft)
        self.label_owner.setStyleSheet('color: rgb((0, 0, 0)')
        self.label_owner.setFont(QFont('微软雅黑', 12))
        self.label_owner.setFixedSize(300, 30)
        self.h_box_owner = QHBoxLayout()
        self.h_box_owner.addWidget(self.label_owner)

        self.label_date_time = QLabel(self)
        self.label_date_time.setText('<b>1997/01/01 00:00:00<b>')
        self.label_date_time.setAlignment(Qt.AlignRight)
        self.label_date_time.setStyleSheet('color: rgb((0, 0, 0)')
        self.label_date_time.setFont(QFont('微软雅黑', 12))
        self.label_date_time.setFixedSize(300, 30)
        self.h_box_date_time = QHBoxLayout()
        self.h_box_date_time.addWidget(self.label_date_time)

        self.h_box_owner_time = QHBoxLayout()
        self.h_box_owner_time.addLayout(self.h_box_owner)
        self.h_box_owner_time.addStretch(1)
        self.h_box_owner_time.addLayout(self.h_box_date_time)

        self.label_select_jid = QLabel(self)
        self.label_select_jid.setText('<b>Jid:<b>')
        self.label_select_jid.setAlignment(Qt.AlignCenter)
        self.label_select_jid.setStyleSheet('color: rgb((0, 0, 0)')
        self.label_select_jid.setFont(QFont('微软雅黑', 10))
        self.label_select_jid.setFixedSize(30, 20)

        self.jid_combobox = QComboBox()
        self.jid_combobox.addItems(["All", "I1", "I2", "I3", "I4", "I5"])
        self.jid_combobox.setFixedSize(100, 20)
        self.h_box_jid_combobox = QHBoxLayout()
        self.h_box_jid_combobox.addWidget(self.label_select_jid)
        self.h_box_jid_combobox.addWidget(self.jid_combobox)

        self.label_select_year = QLabel(self)
        self.label_select_year.setText('<b>Year:<b>')
        self.label_select_year.setAlignment(Qt.AlignCenter)
        self.label_select_year.setStyleSheet('color: rgb((0, 0, 0)')
        self.label_select_year.setFont(QFont('微软雅黑', 10))
        self.label_select_year.setFixedSize(45, 20)

        self.year_combobox = QComboBox()
        self.year_combobox.addItems(["All", "2020", "2021", "2022", "2023", "2024", "2025"])
        self.year_combobox.setFixedSize(100, 20)
        self.h_box_year_combobox = QHBoxLayout()
        self.h_box_year_combobox.addWidget(self.label_select_year)
        self.h_box_year_combobox.addWidget(self.year_combobox)

        self.label_select_month = QLabel(self)
        self.label_select_month.setText('<b>Month:<b>')
        self.label_select_month.setAlignment(Qt.AlignCenter)
        self.label_select_month.setStyleSheet('color: rgb((0, 0, 0)')
        self.label_select_month.setFont(QFont('微软雅黑', 10))
        self.label_select_month.setFixedSize(50, 20)

        self.month_combobox = QComboBox()
        self.month_combobox.addItems(["All", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
        self.month_combobox.setFixedSize(100, 20)
        self.h_box_month_combobox = QHBoxLayout()
        self.h_box_month_combobox.addWidget(self.label_select_month)
        self.h_box_month_combobox.addWidget(self.month_combobox)

        self.label_select_day = QLabel(self)
        self.label_select_day.setText('<b>Day:<b>')
        self.label_select_day.setAlignment(Qt.AlignCenter)
        self.label_select_day.setStyleSheet('color: rgb((0, 0, 0)')
        self.label_select_day.setFont(QFont('微软雅黑', 10))
        self.label_select_day.setFixedSize(35, 20)

        self.day_combobox = QComboBox()
        self.day_combobox.addItems(["All", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"])
        self.day_combobox.setFixedSize(100, 20)
        self.h_box_day_combobox = QHBoxLayout()
        self.h_box_day_combobox.addWidget(self.label_select_day)
        self.h_box_day_combobox.addWidget(self.day_combobox)

        self.label_select_hour = QLabel(self)
        self.label_select_hour.setText('<b>Hour:<b>')
        self.label_select_hour.setAlignment(Qt.AlignCenter)
        self.label_select_hour.setStyleSheet('color: rgb((0, 0, 0)')
        self.label_select_hour.setFont(QFont('微软雅黑', 10))
        self.label_select_hour.setFixedSize(45, 20)

        self.hour_combobox = QComboBox()
        self.hour_combobox.addItems(["All", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"])
        self.hour_combobox.setFixedSize(100, 20)
        self.h_box_hour_combobox = QHBoxLayout()
        self.h_box_hour_combobox.addWidget(self.label_select_hour)
        self.h_box_hour_combobox.addWidget(self.hour_combobox)

        self.button_refresh = QPushButton()
        self.button_refresh.setText("Charting")
        self.button_refresh.setIcon(QIcon('./refresh.ico'))
        self.button_refresh.setStyleSheet('color: rgb((0, 0, 0)')
        self.button_refresh.setFont(QFont('微软雅黑', 12))
        self.button_refresh.setFixedSize(150, 50)
        self.button_refresh.clicked.connect(self.refresh)
        self.h_box_button_refresh = QHBoxLayout()
        self.h_box_button_refresh.addWidget(self.button_refresh)

        self.button_realdata = QPushButton()
        self.button_realdata.setText("Real-time Data")
        self.button_realdata.setIcon(QIcon('./realdata.ico'))
        self.button_realdata.setStyleSheet('color: rgb((0, 0, 0)')
        self.button_realdata.setFont(QFont('微软雅黑', 12))
        self.button_realdata.setFixedSize(200, 50)
        self.button_realdata.clicked.connect(self.realdata)
        self.h_box_button_realdata = QHBoxLayout()
        self.h_box_button_realdata.addWidget(self.button_realdata)

        self.h_box_select_combobox = QHBoxLayout()
        self.h_box_select_combobox.addLayout(self.h_box_jid_combobox)
        self.h_box_select_combobox.addLayout(self.h_box_year_combobox)
        self.h_box_select_combobox.addLayout(self.h_box_month_combobox)
        self.h_box_select_combobox.addLayout(self.h_box_day_combobox)
        self.h_box_select_combobox.addLayout(self.h_box_hour_combobox)
        self.h_box_select_combobox.addLayout(self.h_box_button_refresh)
        self.h_box_select_combobox.addLayout(self.h_box_button_realdata)

        self.label_chart = QLabel(self)
        self.label_chart.setPixmap(QPixmap('./chart_sample.jpeg'))
        self.label_chart.setFixedSize(1300, 600)
        self.label_chart.setScaledContents(True)
        self.h_box_label_chart = QHBoxLayout()
        self.h_box_label_chart.addWidget(self.label_chart)

        self.v_box = QVBoxLayout()
        self.v_box.addLayout(self.h_box_auo_logo_title_time_logo)
        self.v_box.addLayout(self.h_box_owner_time)
        self.v_box.addLayout(self.h_box_select_combobox)
        self.v_box.addLayout(self.h_box_label_chart)
        self.v_box.addStretch(1)

        self.setLayout(self.v_box)

        self.date_time = QtCore.QTimer()  # 创建定时器（定时器类似线程的概念，1.另一线程执行link的函数 2.每隔一定时间执行一次，可实现类似try的概念，单次执行错误，不会退出）
        self.date_time.timeout.connect(self.realtime)  # 到时间后执行函数
        self.date_time.start(1000)  # 每隔10000ms执行一次

        self.log_upload = QtCore.QTimer()  # 创建定时器（定时器类似线程的概念，1.另一线程执行link的函数 2.每隔一定时间执行一次，可实现类似try的概念，单次执行错误，不会退出）
        self.log_upload.timeout.connect(self.upload_log_data)  # 到时间后执行函数
        self.log_upload.start(60000)  # 每隔10000ms执行一次

    def realtime(self):
        self.the_real_time_data_monitor_window._signal.connect(self.getData)

    def getData(self, parameter):
        self.label_date_time.setText("<b>%s<b>" % parameter)

    def refresh(self):
        print("\nStart charting in %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        data_log_analysis(self.jid_combobox.currentText(), self.year_combobox.currentText(), self.month_combobox.currentText(), self.day_combobox.currentText(), self.hour_combobox.currentText())
        self.label_chart.setPixmap(QPixmap('./chart.png'))
        print("\nChart drawing completed in %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        QMessageBox.about(self, "Warm reminder", "Chart drawing completed")

    def realdata(self):
        self.the_real_time_data_monitor_window.show()

    def upload_log_data(self):
        try:  # 使用try避免程式异常终止
            ftp = FTP()  # 建立ftp变量
            ftp.connect(host='10.5.15.163')  # 打开ftp端口
            ftp.login('s06testcode', 's06testcode')  # 使用用户名和密码登录
            buf_size = 1024  # 设定缓存
            fp = open("./data_log.csv", 'rb')  # 打开本地log档文件
            log_name = "Beol_I_Log_Data"
            log_upload = 'smile/B_Beol_I_Monitor_For_MEDA/'  # 设定上传文件夹路径

            ftp.cwd(log_upload)  # 打开上传文件夹
            ftp.storbinary('STOR %s' % log_name, fp, buf_size)  # 上传文件
            print('Log Upload OK')  # 打印此消息到终端

            ftp.set_debuglevel(0)  # 设定debug模式为0
            fp.close()  # 关闭本地log文件
            ftp.quit()  # 断开ftp连接

        except Exception as error:  # try内程序报错时执行下面程序
            print('Log Upload NG, The error is %s' % error)  # 打印错误到终端


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 每一个PyQt5程序中都需要有一个QApplication对象，QApplication类包含在QTWidgets模块中，sys.argv是一个命令行参数列表；Python脚本可以从Shell中执行，比如双击*.py文件，通过参数来选择启动脚本的方式
    form = MainWindow()
    form.show()  # 使用show()方法将窗口控件显示在屏幕上
    sys.exit(app.exec_())  # 进入该程序的主循环;使用sys.exit()方法的退出可以保证程序完整的结束，在这种情况下系统的环境变量会记录程序是如何退出的；如果程序运行成功，exec_()的返回值为0，否则为非0

    pass
