
# -*- coding: utf-8 -*-
import os
#设定文件路径
# path='C:\\Users\\64659\\Desktop\\VOC2007\\JPEGImages\\'
# path='C:\\Users\\48693\\Desktop\\ship\\'
path = 'D:\\图片\\Camera Roll\\'
i=1
#对目录下的文件进行遍历
for file in os.listdir(path):
#判断是否是文件
    if os.path.isfile(os.path.join(path,file))==True:
        if(i<=9):
#设置新文件名
            new_name = file.replace(file,"0000000%d.jpg"%i)
        if(i<=99):
            new_name = file.replace(file, "000000%d.jpg" % i)
        else:
            new_name = file.replace(file, "00000%d.jpg" % i)

#重命名
        os.rename(os.path.join(path,file),os.path.join(path,new_name))
        i+=1
#结束
print ("End")