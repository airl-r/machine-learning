# http://quote.eastmoney.com/center/gridlist.html
import requests
from fake_useragent import UserAgent
import json
import csv
import  urllib.request as r
import threading

def getHtml(url):
    r = requests.get(url, headers={
        'User-Agent': UserAgent().random,
    })
    r.encoding = r.apparent_encoding
    return r.text


# 爬取多少
num = 20

stockUrl = 'http://52.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112409623798991171317_1654957180928&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:80&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1654957180938'


if __name__ == '__main__':
    responseText = getHtml(stockUrl)
    jsonText = responseText.split("(")[1].split(")")[0];
    resJson = json.loads(jsonText)
    datas = resJson['data']['diff']
    dataList = []
    for data in datas:

        row = [data['f12'],data['f14']]
        dataList.append(row)

    print(dataList)

    f = open('stock.csv', 'w+', encoding='utf-8', newline="")
    writer = csv.writer(f)
    writer.writerow(("代码","名称"))
    for data in dataList:
        writer.writerow((data[0]+"\t",data[1]+"\t"))
    f.close()


def getStockList():
    stockList = []
    f = open('stock.csv', 'r', encoding='utf-8')
    f.seek(0)
    reader = csv.reader(f)
    for item in reader:
        stockList.append(item)

    f.close()
    return stockList

def downloadFile(url,filepath):

    try:
        r.urlretrieve(url,filepath)
    except Exception as e:
        print(e)
    print(filepath,"is downLoaded")
    pass

sem = threading.Semaphore(1)

def dowmloadFileSem(url,filepath):
    with sem:
        downloadFile(url,filepath)

urlStart = 'http://quotes.money.163.com/service/chddata.html?code='
urlEnd = '&end=20210221&fields=TCLOSW;HIGH;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER'

if __name__ == '__main__':
    stockList = getStockList()
    stockList.pop(0)
    print(stockList)


    for s in stockList:
        scode = str(s[0].split("\t")[0])

        url = urlStart+("0" if scode.startswith('6') else '1')+ scode + urlEnd

        print(url)
        filepath = (str(s[1].split("\t")[0])+"_"+scode)+".csv"
        threading.Thread(target=dowmloadFileSem,args=(url,filepath)).start()



















