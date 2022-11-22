from math import pi, sin, cos
import matplotlib.pyplot as plt
no_pieces = 100
dt = 2*pi/no_pieces
t = 0
vx = []
vy = []
while t <= 2*pi:
    vx.append(16*sin(t)**3)
    vy.append(13*cos(t)-5*cos(2*t)-2*cos(3*t)-cos(4*t))
    t += dt
plt.plot(vx, vy)
plt.show()