# -*- coding: utf-8 -*-
"""
@Time    : 2020/7/2 17:49
@Author  : Xiaofei
@Contact : smile.qiangqian@Gmail.com
@File    : data_log_analysis.py
@Version : 1.0
@IDE     : PyCharm
@Source  : python -m pip install *** -i https://pypi.tuna.tsinghua.edu.cn/simple
"""

import os
import sys

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']  # Prevent packaging errors on windows system

import pandas as pd

import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt


def data_log_analysis(jid, year, month, day, hour):

    if month[0] == "0":
        month = month[1]
    if day[0] == "0":
        day = day[1]
    if hour[0] == "0":
        hour = hour[1]
    print("\n" + str([jid, year, month, day, hour]) + " and Data Clean Start")
    csv_data = pd.read_csv("./data_log.csv")
    csv_df = pd.DataFrame(csv_data)

    if year == "All":
        csv_df_year = csv_df
    if year != "All":
        bool_year = csv_df["Date_Time"].str.contains('%s/' % year)
        filter_data_year = csv_df[bool_year]
        csv_df_year = filter_data_year

    if month == "All":
        csv_df_year_month = csv_df_year
    if month != "All":
        bool_year_month = csv_df_year["Date_Time"].str.contains('/%s/' % month)
        filter_data_year_month = csv_df_year[bool_year_month]
        csv_df_year_month = filter_data_year_month

    if day == "All":
        csv_df_year_month_day = csv_df_year_month
    if day != "All":
        bool_year_month_day = csv_df_year_month["Date_Time"].str.contains('/%s' % day + " ")
        filter_data_year_month_day = csv_df_year_month[bool_year_month_day]
        csv_df_year_month_day = filter_data_year_month_day

    if hour == "All":
        csv_df_year_month_day_hour = csv_df_year_month_day
    if hour != "All":
        bool_year_month_day_hour = csv_df_year_month_day["Date_Time"].str.contains(" " + '%s' % hour + ":")
        filter_data_year_month_day_hour = csv_df_year_month_day[bool_year_month_day_hour]
        csv_df_year_month_day_hour = filter_data_year_month_day_hour

    if jid == "All":
        data_year_month_day_hour_jid_list = csv_df_year_month_day_hour["I1"].tolist() + csv_df_year_month_day_hour["I2"].tolist() + csv_df_year_month_day_hour["I3"].tolist() + csv_df_year_month_day_hour["I4"].tolist() + csv_df_year_month_day_hour["I5"].tolist()
    if jid != "All":
        data_year_month_day_hour_jid_list = csv_df_year_month_day_hour["%s" % jid].tolist()

    print("The Data is %s" % data_year_month_day_hour_jid_list)
    sns.set_palette("hls")
    mpl.rc("figure", figsize=(13.66, 6.00))
    sns.distplot(data_year_month_day_hour_jid_list, bins=100, kde_kws={"color": "seagreen", "lw": 3}, hist_kws={"color": "b"})
    plt.xlim(-0.5, 100)
    plt.xlabel('Current-Value')  # 绘制x轴
    plt.ylabel('Probability')  # 绘制y轴
    plt.title(r'Histogram : ND Beol Current Intelligent Analysis')
    plt.savefig('./chart.png')  # 保存图片
    plt.clf()


if __name__ == "__main__":
    data_log_analysis()
    pass
