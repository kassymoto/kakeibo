from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from .models import Post
from .forms import MyForm
from django.http import QueryDict
import os
import csv
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def kakeibo(request):
    d =[]
    if request.method=="POST":
        form = MyForm(data=request.POST)

        if not os.path.exists("./kakeibo.csv"):
            open("./kakeibo.csv", "w").close()
        save_csv(str(dict(request.POST)['category'][0]), str(dict(request.POST)['text'][0]))
        d = get_csv()

        if form.is_valid():
            pass
    else:
        form = MyForm()

    form = MyForm()
    cs = category_sum(d)
    plot_graph(cs)
    return render(request, 'blog/kakeibo.html', {
        'form': form,
        'data' : d,
        'category_sum' : cs,
    })

def plot_graph(cs):
    data=cs.values()
    label=cs.keys()
    os.remove('blog/static/images/simple.png')
    ###綺麗に書くためのおまじない###
    plt.style.use('ggplot')
    plt.rcParams.update({'font.size':15})

    ###各種パラメータ###
    size=(9,5) #凡例を配置する関係でsizeは横長にしておきます。
    col=cm.Spectral(np.arange(len(data))/float(len(data))) #color指定はcolormapから好みのものを。

    ###pie###
    plt.figure(figsize=size,dpi=100)
    plt.pie(data,colors=col,counterclock=False,startangle=90,autopct=lambda p:'{:.1f}%'.format(p) if p>=5 else '')
    plt.subplots_adjust(left=0,right=0.7)
    plt.legend(label,fancybox=True,loc='center left',bbox_to_anchor=(0.9,0.5))
    plt.axis('equal')
    plt.savefig('blog/static/images/simple.png',bbox_inches='tight',pad_inches=0.05)
    plt.close()

def save_csv(category, price):
    #CSVを開く
    with open('./kakeibo.csv', 'a') as f:
        #CSVに書き込みを行う
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow([category, price])

def get_csv():

    csv_list = []
    tmp = []
    #CSVファイルを開く
    with open('./kakeibo.csv', 'r') as f:
        #ファイルから一行読み込み
        reader = csv.reader(f)
        #rowは配列として各列のセルの情報を格納してあるので、各々をリストに辞書型としてアペンドする
        for row in reader:
            tmp.append(row[0])
            tmp.append(row[1])
            csv_list.append(tmp)
            tmp = []
    #読み込んだしたチャットデータを返す
    return csv_list

def category_sum(d):
    cs = {}
    for i in d:
        key, num = i[0], int(i[1])
        if key in cs:
            cs[key]+=num
        else:
            cs[key]=num
        print(cs)
    return cs
