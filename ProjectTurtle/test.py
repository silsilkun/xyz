import turtle as t
from random import random
import math

# 스피로 그래프
def spirograph():
    t.pensize(2)
    for i in range(100):
        t.circle(100)
        t.left(360 / 100)

# 2. 프랙탈 같은 별 패턴
def star_pattern():
    t.pensize(1)
    for i in range(200):
        t.forward(i * 2)
        t.left(144)

# 3. 나선형 곡선
def spiral():
    t.pensize(2)
    for i in range(200):
        t.forward(i * 2)
        t.right(59)

# 4. 로즈 곡선 (꽃 모양)
def rose_curve():
    t.pensize(2)
    t.penup()
    for angle in range(0, 360 * 5, 5):  # 여러 번 반복
        r = 200 * math.sin(math.radians(5 * angle))  # k=5
        x = r * math.cos(math.radians(angle))
        y = r * math.sin(math.radians(angle))
        t.goto(x, y)
        t.pendown()


rose_curve()

t.mainloop()
