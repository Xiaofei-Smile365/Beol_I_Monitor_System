# -*- coding: utf-8 -*-
"""
@Time    : 2020/6/24 15:30
@Author  : Xiaofei
@Contact : smile.qiangqian@Gmail.com
@File    : real_time_data_monitor.py
@Version : 1.0
@IDE     : PyCharm
@Source  : python -m pip install *** -i https://pypi.tuna.tsinghua.edu.cn/simple
"""
import sys
import os

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']  # Prevent packaging errors on windows system

import serial

import sys  # 载入必需的模块
import os

import datetime
import pandas as pd

from PyQt5.QtGui import *
import pyqtgraph as pg

from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap

from PyQt5 import QtCore
from PyQt5.QtWidgets import *  # 在Qt5中使用的基本的GUI窗口控件都在PyQt5.QtWidgets模块中


# 二级界面
class Real_time_data_monitor(QWidget):
    # 定义信号
    _signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle('ND Beol 电流实时监控平台')
        self.setWindowIcon(QIcon('./plotform.ico'))  # 设定窗口的图标
        self.setFixedSize(1366, 768)

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap('./background_blue.jpg').scaled(self.width(), self.height())))  # 设定UI界面背景图片
        self.setPalette(palette)
        self.setFixedSize(1366, 768)

        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        self.receive_text = QPushButton(self)
        self.receive_text.setText('<b>实时接收到-Hex数据<b>')
        self.receive_text.setStyleSheet('color: rgb(0, 0, 255)')
        self.receive_text.setFont(QFont('SanSerif', 8))
        self.receive_text.setFixedSize(1340, 50)

        self.receive_text_i1 = QPushButton(self)
        self.receive_text_i1.setText('<b>I1<b>')
        self.receive_text_i1.setStyleSheet('color: rgb(0, 0, 255)')
        self.receive_text_i1.setFont(QFont('SanSerif', 16))
        self.receive_text_i1.setFixedSize(100, 100)

        self.receive_text_i2 = QPushButton(self)
        self.receive_text_i2.setText('<b>I2<b>')
        self.receive_text_i2.setStyleSheet('color: rgb(0, 0, 255)')
        self.receive_text_i2.setFont(QFont('SanSerif', 16))
        self.receive_text_i2.setFixedSize(100, 100)

        self.receive_text_i3 = QPushButton(self)
        self.receive_text_i3.setText('<b>I3<b>')
        self.receive_text_i3.setStyleSheet('color: rgb(0, 0, 255)')
        self.receive_text_i3.setFont(QFont('SanSerif', 16))
        self.receive_text_i3.setFixedSize(100, 100)

        self.receive_text_i4 = QPushButton(self)
        self.receive_text_i4.setText('<b>I4<b>')
        self.receive_text_i4.setStyleSheet('color: rgb(0, 0, 255)')
        self.receive_text_i4.setFont(QFont('SanSerif', 16))
        self.receive_text_i4.setFixedSize(100, 100)

        self.receive_text_i5 = QPushButton(self)
        self.receive_text_i5.setText('<b>I5<b>')
        self.receive_text_i5.setStyleSheet('color: rgb(0, 0, 255)')
        self.receive_text_i5.setFont(QFont('SanSerif', 16))
        self.receive_text_i5.setFixedSize(100, 100)

        self.plot_plt_01 = pg.PlotWidget()
        self.plot_plt_01.showGrid(x=True, y=True)
        self.plot_plt_01.setYRange(0, 50)
        self.data_list_01 = []

        self.plot_plt_02 = pg.PlotWidget()
        self.plot_plt_02.showGrid(x=True, y=True)
        self.plot_plt_02.setYRange(0, 50)
        self.data_list_02 = []

        self.plot_plt_03 = pg.PlotWidget()
        self.plot_plt_03.showGrid(x=True, y=True)
        self.plot_plt_03.setYRange(0, 50)
        self.data_list_03 = []

        self.plot_plt_04 = pg.PlotWidget()
        self.plot_plt_04.showGrid(x=True, y=True)
        self.plot_plt_04.setYRange(0, 50)
        self.data_list_04 = []

        self.plot_plt_05 = pg.PlotWidget()
        self.plot_plt_05.showGrid(x=True, y=True)
        self.plot_plt_05.setYRange(0, 50)
        self.data_list_05 = []

        self.main_layout.addWidget(self.receive_text, 0, 0, 1, 2)
        self.main_layout.addWidget(self.receive_text_i1, 1, 0)
        self.main_layout.addWidget(self.plot_plt_01, 1, 1)
        self.main_layout.addWidget(self.receive_text_i2, 2, 0)
        self.main_layout.addWidget(self.plot_plt_02, 2, 1)
        self.main_layout.addWidget(self.receive_text_i3, 3, 0)
        self.main_layout.addWidget(self.plot_plt_03, 3, 1)
        self.main_layout.addWidget(self.receive_text_i4, 4, 0)
        self.main_layout.addWidget(self.plot_plt_04, 4, 1)
        self.main_layout.addWidget(self.receive_text_i5, 5, 0)
        self.main_layout.addWidget(self.plot_plt_05, 5, 1)

        self.open_com()

    def open_com(self):
        for n in range(0, 255):
            self.ser = serial.Serial("COM%s" % int(n+1), 115200, timeout=0.5)
            if self.ser.is_open is True:
                break

        self.data_mark = 0
        self.date_time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data_mark_num = 0
        self.no_data_mark_num = 0

        self.data_i1 = 0
        self.data_i2 = 0
        self.data_i3 = 0
        self.data_i4 = 0
        self.data_i5 = 0

        self.data_list = []

        if os.path.exists("./data_log.csv") is False:
            print("\nLog file does not exist in %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            print("\nStart creating log file in %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            data_log = open("./data_log.csv", 'w')
            log_columns = ['Date_Time', 'I1', 'I2', 'I3', 'I4', 'I5']  # 写入表头
            print("The columns is %s" % log_columns)
            data = pd.DataFrame(columns=log_columns)  # 转换格式
            data.to_csv(data_log, index=False)  # 写入到log
            data_log.close()  # 关闭文件
            print("Log file creation completed in %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        else:
            print("\nLog file already exists in %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            pass

        self.get_232 = QtCore.QTimer()  # 创建定时器（定时器类似线程的概念，1.另一线程执行link的函数 2.每隔一定时间执行一次，可实现类似try的概念，单次执行错误，不会退出）
        self.get_232.timeout.connect(self.receive)  # 到时间后执行函数
        self.get_232.start(1000)  # 每隔10000ms执行一次

    def receive(self):
        print("\nStart Receive Real-Data in %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if len(self.data_list_01) == 500:
            self.plot_plt_01 = pg.PlotWidget()
            self.plot_plt_01.showGrid(x=True, y=True)
            self.plot_plt_01.setYRange(0, 50)
            self.data_list_01 = []

            self.plot_plt_02 = pg.PlotWidget()
            self.plot_plt_02.showGrid(x=True, y=True)
            self.plot_plt_02.setYRange(0, 50)
            self.data_list_02 = []

            self.plot_plt_03 = pg.PlotWidget()
            self.plot_plt_03.showGrid(x=True, y=True)
            self.plot_plt_03.setYRange(0, 50)
            self.data_list_03 = []

            self.plot_plt_04 = pg.PlotWidget()
            self.plot_plt_04.showGrid(x=True, y=True)
            self.plot_plt_04.setYRange(0, 50)
            self.data_list_04 = []

            self.plot_plt_05 = pg.PlotWidget()
            self.plot_plt_05.showGrid(x=True, y=True)
            self.plot_plt_05.setYRange(0, 50)
            self.data_list_05 = []

            self.main_layout.addWidget(self.receive_text, 0, 0, 1, 2)
            self.main_layout.addWidget(self.receive_text_i1, 1, 0)
            self.main_layout.addWidget(self.plot_plt_01, 1, 1)
            self.main_layout.addWidget(self.receive_text_i2, 2, 0)
            self.main_layout.addWidget(self.plot_plt_02, 2, 1)
            self.main_layout.addWidget(self.receive_text_i3, 3, 0)
            self.main_layout.addWidget(self.plot_plt_03, 3, 1)
            self.main_layout.addWidget(self.receive_text_i4, 4, 0)
            self.main_layout.addWidget(self.plot_plt_04, 4, 1)
            self.main_layout.addWidget(self.receive_text_i5, 5, 0)
            self.main_layout.addWidget(self.plot_plt_05, 5, 1)
        self.data_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.rec = self.ser.read(200)
        self._signal.emit(self.data_time)
        if str(self.rec) != "b''" and len(self.rec) == 190:
            print("\nreceive == ", self.rec)

            self.receive_text.setText(str(self.rec))

            i1 = round((int(str(str(self.rec)[11:13] + str(self.rec)[9:11]), 16) / 10))
            print("\nI1 == %s" % i1)
            self.receive_text_i1.setText(str(i1))
            self.data_list_01.append(i1)
            self.plot_plt_01.plot().setData(self.data_list_01, pen="g")

            i2 = round((int(str(str(self.rec)[19:21] + str(self.rec)[17:19]), 16) / 10))
            print("I2 == %s" % i2)
            self.receive_text_i2.setText(str(i2))
            self.data_list_02.append(i2)
            self.plot_plt_02.plot().setData(self.data_list_02, pen="g")

            i3 = round((int(str(str(self.rec)[27:29] + str(self.rec)[25:27]), 16) / 10))
            print("I3 == %s" % i3)
            self.receive_text_i3.setText(str(i3))
            self.data_list_03.append(i3)
            self.plot_plt_03.plot().setData(self.data_list_03, pen="g")

            i4 = round((int(str(str(self.rec)[35:37] + str(self.rec)[33:35]), 16) / 10))
            print("I4 == %s" % i4)
            self.receive_text_i4.setText(str(i4))
            self.data_list_04.append(i4)
            self.plot_plt_04.plot().setData(self.data_list_04, pen="g")

            i5 = round((int(str(str(self.rec)[43:45] + str(self.rec)[41:43]), 16) / 10))
            print("I5 == %s" % i5)
            self.receive_text_i5.setText(str(i5))
            self.data_list_05.append(i5)
            self.plot_plt_05.plot().setData(self.data_list_05, pen="g")

            if 50 >= i1 >= 30 or 50 >= i2 >= 30 or 50 >= i3 >= 30 or 50 >= i4 >= 30 or 50 >= i5 >= 30:
                self.data_mark = 1
                print("\nThe Data mark set 1 in %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                self.data_mark = 0
                print("\nThe Data mark set 0 in %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            if self.data_mark == 1:
                self.data_mark_num = self.data_mark_num + 1
                if self.data_mark_num == 3:
                    self.no_data_mark_num = 0
                    print("\nThe no Data mark num cleared successfully in %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                    print("\nData start writing in %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    self.date_time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Data Start Writing
                    self.data_i1 = i1
                    self.data_i2 = i2
                    self.data_i3 = i3
                    self.data_i4 = i4
                    self.data_i5 = i5

                    self.data_list = [[self.date_time_now, self.data_i1, self.data_i2, self.data_i3, self.data_i4, self.data_i5]]
                    print("The Data is %s" % self.data_list)
                    data = pd.DataFrame(self.data_list)
                    data.to_csv("./data_log.csv", mode='a', header=False, index=False)  # 追加模式写入到新文件
                    print("\nData written successfully in %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    pass
            else:
                self.no_data_mark_num = self.no_data_mark_num + 1
                if self.no_data_mark_num == 3:
                    self.data_mark_num = 0
                    print("\nThe Data mark num cleared successfully in %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    pass
        else:
            pass

        self.data_mark = 0
        print("The Data mark set 0 in %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("\nEnd Receive Real-Data in %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    app = QApplication(
        sys.argv)  # 每一个PyQt5程序中都需要有一个QApplication对象，QApplication类包含在QTWidgets模块中，sys.argv是一个命令行参数列表；Python脚本可以从Shell中执行，比如双击*.py文件，通过参数来选择启动脚本的方式
    form = Real_time_data_monitor()
    form.show()  # 使用show()方法将窗口控件显示在屏幕上
    sys.exit(
        app.exec_())  # 进入该程序的主循环;使用sys.exit()方法的退出可以保证程序完整的结束，在这种情况下系统的环境变量会记录程序是如何退出的；如果程序运行成功，exec_()的返回值为0，否则为非0

    pass
