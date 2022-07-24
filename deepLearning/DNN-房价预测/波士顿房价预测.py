## 深度学习框架
import paddle

import numpy as np
import os
import matplotlib.pyplot as plt



## 绘图

Batch = 0
Batchs = []
all_train_accs = []
def draw_train_acc(Batchs,train_accs):
    title = "training accs"
    plt.title(title)
    plt.xlabel("batch")
    plt.ylabel("acc")
    plt.plot(Batchs, train_accs, color = 'green', label = 'training accs')
    plt.legend()
    plt.grid()
    plt.show()


all_train_loss = []
def draw_train_loss(Batchs,train_loss):
    title = "training loss"
    plt.title(title)
    plt.xlabel("batch")
    plt.ylabel("loss")
    plt.plot(Batchs, train_loss, color = 'red', label = 'training loss')
    plt.legend()
    plt.grid()
    plt.show()

## 绘制真实值与预测值的对比图
def draw_infer_result(groud_truths, infer_results):
    title = 'Boston'
    plt.title(title)
    x = np.arange(1,20)
    y = x
    plt.plot(x,y);
    plt.xlabel("ground truth")
    plt.ylabel("infer result")
    plt.scatter(groud_truths,infer_results,color='green',label='training cost')
    plt.grid()
    plt.show()


'''
数据集加载
'''

train_dataset = paddle.text.datasets.UCIHousing(mode="train")
eval_dataset = paddle.text.datasets.UCIHousing(mode="test")

train_loader = paddle.io.DataLoader(train_dataset,batch_size=32, shuffle=True)
eval_loader = paddle.io.DataLoader(eval_dataset,batch_size=8,shuffle=False)

print(train_dataset[1])


'''
核心

网络搭建
'''

class MyDNN(paddle.nn.Layer):
    def __init__(self):
        super(MyDNN, self).__init__()

        #self.linear1 = paddle.nn.Linear(13,1,None) #全连接层，paddle.nn.Linear(in_features,out_features,weight)

        self.linear1 = paddle.nn.Linear(13, 32, None)

        self.linear2 = paddle.nn.Linear(32, 64, None)

        self.linear3 = paddle.nn.Linear(64, 32, None)

        self.linear4 = paddle.nn.Linear(32, 1, None)
    def forward(self, inputs): ## 传播函数
        x = self.linear1(inputs)
        x = self.linear2(x)
        x = self.linear3(x)
        x = self.linear4(x)
        return x


'''
网络训练与测试
'''


## 实例化
model = MyDNN()
model.train()
mse_loss = paddle.nn.MSELoss()
opt = paddle.optimizer.SGD(learning_rate=0.001, parameters=model.parameters())
epochs_num = 300


for epochs in range(epochs_num):
    for batch_id,data in enumerate(train_loader()):
        feature = data[0]
        label = data[1]
        predict = model(feature)
        loss = mse_loss(predict, label)
        loss.backward()
        opt.step()
        opt.clear_grad()
        if batch_id!=0 and batch_id%10 == 0:
            Batch = Batch+10
            Batchs.append(Batch)
            all_train_loss.append(loss.numpy()[0])
            print("epoch{},step:{},train_loss:{}".format(epochs,batch_id,loss.numpy()[0]))

paddle.save(model.state_dict(),"UCIHousingDNN")
draw_train_loss(Batchs,all_train_loss)




para_state = paddle.load("UCIHousingDNN")
model = MyDNN()
model.eval()
model.set_state_dict(para_state)
losses = []
for batch_id,data in enumerate(eval_loader()):
    feature = data[0]
    label = data[1]
    predict = model(feature)
    loss = mse_loss(predict,label)
    losses.append(loss.numpy()[0])
avg_loss = np.mean(losses)
print(avg_loss)