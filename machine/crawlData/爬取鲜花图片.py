import requests
import os
import urllib

class GetImage():
    def __init__(self,keyword='鲜花',paginator=1):
        self.url = 'http://image.baidu.com/search/acjson?'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }

        self.keyword = keyword
        self.paginator = paginator


    def get_param(self):

        keyword = urllib.parse.quote(self.keyword)
        params = []

        for i in range(1,self.paginator+1):
            params.append(
                #'tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&latest=0&copyright=0&word={}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&cg=star&pn={}&rn=30&gsm=78&1557125391211='.format(keyword,keyword,30*i)
                'tn=resultjson_com&logid=10338332981203604364&ipn=rj&ct=201326592&is=&fp=result&fr=&word={}&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&expermode=&nojc=&isAsync=&pn={}&rn=30&gsm=78&1650241802208='.format(keyword,keyword,30*i)

            )
        return params
    def get_urls(self,params):
        urls = []
        for param in params:
            urls.append(self.url+param)
        return urls

    def get_image_url(self,urls):
        image_url = []
        for url in urls:
            json_data = requests.get(url,headers = self.headers).json()
            json_data = json_data.get('data')
            for i in json_data:
                if i:
                    image_url.append(i.get('thumbURL'))
        return image_url
    def get_image(self,image_url):
        ##根据图片url，存入图片
        file_name = os.path.join(".",self.keyword)
        #print(file_name)
        if not os.path.exists(file_name):
            os.makedirs(file_name)

        for index,url in enumerate(image_url,start=1):
            with open(file_name+'/{}.jpg'.format(index),'wb') as f:
                f.write(requests.get(url,headers=self.headers).content)

            if index != 0 and index%30 == 0:
                print("第{}页下载完成".format(index/30))


    def __call__(self, *args, **kwargs):
        params = self.get_param()
        urls = self.get_urls(params)
        image_url = self.get_image_url(urls)
        self.get_image(image_url=image_url)


if __name__ == '__main__':
    spider = GetImage('鲜花',3)
    spider()









