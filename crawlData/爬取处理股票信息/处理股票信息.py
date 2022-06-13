## 主要利用matplotlib进行图像绘制

import pandas as pd
import matplotlib.pyplot as plt
import csv
import 股票数据爬取 as gp

plt.rcParams['font.sans-serif'] = ['simhei'] #指定字体
plt.rcParams['axes.unicode_minus'] = False #显示-号
plt.rcParams['figure.dpi'] = 100 #每英寸点数

files = []

def read_file(file_name):
    data = pd.read_csv(file_name,encoding='gbk')
    col_name = data.columns.values
    return data,col_name

def get_file_path():
    stock_list = gp.getStockList()
    paths = []
    for stock in stock_list[1:]:
        p = stock[1].strip()+"_"+stock[0].strip()+".csv"
        print(p)
        data,_=read_file(p)
        if len(data)>1:
            files.append(p)
            print(p)

get_file_path()
print(files)

def get_diff(file_name):
    data,col_name = read_file(file_name)
    index = len(data['日期'])-1
    sep = index//15
    plt.figure(figsize=(15,17))

    x = data['日期'].values.tolist()
    x.reverse()

    xticks = list(range(0,len(x),sep))
    xlabels = [x[i] for i in xticks]
    xticks.append(len(x))


    y1 = [float(c) if c!='None' else 0 for c in data['涨跌额'].values.tolist()]
    y2 = [float(c) if c != 'None' else 0 for c in data['涨跌幅'].values.tolist()]

    y1.reverse()
    y2.reverse()

    ax1 = plt.subplot(211)
    plt.plot(range(1,len(x)+1),y1,c='r')
    plt.title('{}-涨跌额/涨跌幅'.format(file_name.split('_')[0]),fontsize = 20)
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xlabels,rotation = 40)
    plt.ylabel('涨跌额')

    ax2 = plt.subplot(212)
    plt.plot(range(1, len(x) + 1), y1, c='g')
    #plt.title('{}-涨跌额/涨跌幅'.format(file_name.splir('_')[0]), fontsize=20)
    ax2.set_xticks(xticks)
    ax2.set_xticklabels(xlabels, rotation=40)
    plt.xlabel('日期')
    plt.ylabel('涨跌额')
    plt.show()


print(len(files))
for file in files:
    get_diff(file)