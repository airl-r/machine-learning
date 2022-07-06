## 数据集 sklearn中


import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import colors

from sklearn import svm
from sklearn import model_selection


## 加载数据集

def iris_type(s):
    it = {b'Iris-setosa':0, b'Iris-versicolor':1, b'Iris-virginica':2}
    return it[s]


data = np.loadtxt('Iris-data/iris.data',dtype=float,delimiter=',',converters={4:iris_type})

x,y = np.split(data, (4, ), axis=1)

x = x[:,:2]
x_train,x_test, y_train, y_test = model_selection.train_test_split(x,y,random_state=1,test_size=0.2)


## 构建SVM分类器，训练函数

def classifier():
    clf = svm.SVC(C=0.8, kernel='linear', decision_function_shape='ovr')
    return clf

def train(clf, x_train, y_train):
    clf.fit(x_train, y_train.ravel())


clf = classifier()
train(clf,x_train,y_train)

## 初始化分类器，训练模型
def show_accuracy(a, b, tip):
    acc = a.ravel()==b.ravel()
    print('%s accracy:%.3f'%(tip, np.mean(acc)))

## 展示训练结果，及验证结果

def print_accracy(clf, x_train, y_train, x_test, y_test):
    print('training prediction:%.3f'%(clf.score(x_train, y_train)))
    print('test prediction:%.3f'%(clf.score(x_test, y_test)))

    show_accuracy(clf.predict(x_train),y_train, 'training data')
    show_accuracy(clf.predict(x_test), y_test, 'testing data')

    print('decision_function:\n',clf.decision_function(x_train)[:2])

print_accracy(clf, x_train, y_train, x_test, y_test)



def draw(clf, x):
    iris_feature = 'sepal length', 'sepal width', 'petal length', 'petal width'

    x1_min,x1_max = x[:,0].min(), x[:,0].max()
    x2_min,x2_max = x[:,1].min(), x[:,1].max()

    x1, x2 = np.mgrid[x1_min:x1_max:200j, x2_min:x2_max:200j]

    grid_test = np.stack((x1.flat, x2.flat), axis=1)
    print('grid_test:\n',grid_test[:2])

    z = clf.decision_function(grid_test)
    print('the distance:',z[:2])

    grid_hat = clf.predict(grid_test)
    print(grid_hat[:2])


    grid_hat = grid_hat.reshape(x1.shape)
    cm_light = mpl.colors.ListedColormap(['#A0FFA0', '#FFA0A0', '#A0A0FF'])
    cm_dark = mpl.colors.ListedColormap(['g', 'b', 'r'])

    plt.pcolormesh(x1, x2, grid_hat, cmap=cm_light)
    plt.scatter(x[:,0], x[:, 1],c=np.squeeze(y), edgecolors='k', s=50, cmap=cm_dark)
    plt.scatter(x_test[:,0],x_test[:,1], s=120, facecolor='none', zorder=10)
    plt.xlabel(iris_feature[0])
    plt.ylabel(iris_feature[1])
    plt.xlim(x1_min, x1_max)
    plt.ylim(x2_min, x2_max)
    plt.title('Iris data classification via SVM')
    plt.grid()
    plt.show()

draw(clf, x)
