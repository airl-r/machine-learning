# 获取教程、习题、案例，共同学习、讨论、打卡
# 请关注：Crossin的编程教室
# 如果运行代码遇到问题，可加群讨论 - QQ群：155816967
# 如用代码进行二创并发布，请在明显处注明来源：Crossin的编程教室，否则将可能成为我下期视频素材[狗头][冷笑]

# 代码使用到 pygame-zero 框架，看起来与一般代码稍有不同，会有很多未定义的方法和变量，
# 在一些编辑器里会报错，但其实是可以运行的，无需手动增加 import。
# pgzero有两种方式运行（https://pygame-zero.readthedocs.io/zh_CN/latest/ide-mode.html）
# 本代码用的是第二种直接运行的方式（需新版pgzero）。
# 有部分读者反馈此代码在spyder上无法运行，类似情况可以尝试第一种传统方法：
# 把最后的pgzrun.go()去掉，然后直接在命令行该目录下运行： pgzrun sheep.py

# cv2模块也需要安装： pip install  opencv-python

import pgzrun
from math import pi, sin, cos
import random
import cv2

# 读取原始视频，需自己放置一个video.mp4在代码文件夹下，如需demo视频可加群索取


video = cv2.VideoCapture('video.mp4')

# 粒子类，图像上每一个小点都是一个粒子对象
class Particle():
    def __init__(self, pos, size, f):
        self.pos = pos    # 粒子当前位置（后面会变动）
        self.pos0 = pos   # 粒子的原始位置
        self.size = size  # 粒子大小
        self.f = f        # 粒子的随机位移比例

    def draw(self):
        global L
        # 用矩形绘制粒子
        screen.draw.filled_rect(Rect((L*self.f*self.pos[0] + 400, -L*self.f*self.pos[1] + 300), self.size), 'hot pink')

    def update(self, t):
        # 根据程序运行时间计算一个正弦函数作为位移量
        # 如果要调整爱心跳动的频率、幅度等效果，可修改这里面的数字
        df = 1 + (4 - 3 * self.f) * sin(t * 3) / 12
        self.pos = self.pos0[0] * df, self.pos0[1] * df

tt = [105, 102, 98, 115, 117, 33, 112, 103, 33, 106, 108, 118, 111, 33, 46, 33, 68, 115, 112, 116, 116, 106, 111, 30341, 32535, 31244, 25946, 23461]
no_p = 20000
dt = 2*pi/no_p
particles = []
t = 0
c = 0
# 采用极坐标下的爱心曲线，计算出爱心图案上的基准点，创建粒子对象
# 每个点会有一个延轴向的随机位移，随机采用正态分布
while t < 2*pi:
    c += 1
    sigma = 0.15 if c % 5 else 0.3
    f = 1 - abs(random.gauss(1, sigma) - 1)
    x = 16*sin(t)**3
    y = 13*cos(t)-5*cos(2*t)-2*cos(3*t)-cos(4*t)
    size = (random.uniform(0.5,2.5), random.uniform(0.5,2.5))
    particles.append(Particle((x, y), size, f))
    t += dt

def draw():
    if status == 3:
        # 读取视频每一帧
        hasFrame, frame = video.read()
        if not hasFrame:
            exit()
        global count
        count += 1
        # 为了提升运行效率，这里每3帧绘制一次，其它帧直接跳过
        if count % 3:
            return
        screen.clear()
        # 视频长宽
        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]
        # 转灰度图
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 缩小图片并调整长宽比
        img_resize = cv2.resize(img_gray, (int(frameWidth / 10), int(frameHeight / 10)))
        img_resize[0][64] = 16
        # 遍历图片中的像素
        for j, row in enumerate(img_resize):
            for k, pixel in enumerate(row):
                # 根据像素灰度值，确定绘制方块的大小
                w = pixel / 32 * random.uniform(0.8, 1)
                # 在对应像素处绘制方块
                screen.draw.filled_rect(Rect((k*6*L+(16+400-400*L), j*8*L+(16+300-300*L)), (w, w)), 'hot pink')
    else:
        screen.clear()
        # 绘制爱心粒子
        for p in particles:
            p.draw()
        if status == 1:
            # 采用同样原理，绘制外层大爱心，但生成粒子，只是每帧随机绘制
            t = 0
            while t < 2*pi:
                f = random.gauss(1.1, 0.1)
                x = 16*sin(t)**3
                y = 13*cos(t)-5*cos(2*t)-2*cos(3*t)-cos(4*t)
                size = (random.uniform(0.5,2.5), random.uniform(0.5,2.5))
                screen.draw.filled_rect(Rect((10*f*x + 400, -10*f*y + 300), size), 'hot pink')
                t += dt * 3
    screen.draw.filled_rect(Rect((-10*11 + 400, 11*20 + 200), (2, 2)), 'hot pink')

TITLE = ''.join([chr(i-1) for i in tt])
status = 0
L = 50
elapsed = 0
count = 0
def update(dt):
    global elapsed, L, status
    elapsed += dt
    # 按下空格，切换到视频效果
    if keyboard.SPACE:
        status = 2
    if status == 0:
        # 为了初始的集聚效果，加了一个很大的倍数L，并不断缩小至正常值
        L -= dt * 100
        if L <= 10:
            status = 1
            L = 10
    elif status == 2:
        # 按下空格后的扩散效果
        L += dt * 100
        if L > 50:
            status = 3
    elif status == 3 and L > 1:
        # 二次集聚效果
        L *= 0.9
        if L <= 1:
            L = 1
    # 根据时间更新粒子位置
    for p in particles:
        p.update(elapsed)

pgzrun.go()

