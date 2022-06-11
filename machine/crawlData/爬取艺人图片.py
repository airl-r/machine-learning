import requests
import json
import os
import urllib

def getPicinfo(url):
    headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',

    }
    response = requests.get(url,headers)

    if response.status_code == 200:
        return response.text
    return None


Download_dir = 'picture'
if os.path.exists(Download_dir) == False:
    os.mkdir(Download_dir)


pn_num = 1
rn_num = 10

for k in range(pn_num):
    url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=28266&from_mid=500&format=json&ie=utf-8&oe=utf-8&query=%E4%B8%AD%E5%9B%BD%E8%89%BA%E4%BA%BA&sort_key=&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn="+str(pn_num)+"&rn="+str(rn_num)+"&_=1580457480665"
    res = getPicinfo(url)
    json_str = json.loads(res)
    figs = json_str['data'][0]['result']

    for i in figs:
        name = i['ename']
        img_url = i['pic_4n_78']
        img_res = requests.get(img_url)
        if img_res.status_code == 200:
            ext_str_splits = img_res.headers['Content-Type'].split('/')
            ext = ext_str_splits[-1]
            fname = name+'.'+ext
            open(os.path.join(Download_dir,fname),'wb').write(img_res.content)

            print(name,img_url,'saved')



















