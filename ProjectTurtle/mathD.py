import turtle
import math
import random
import time

# 설정
screen = turtle.Screen()
screen.setup(1000, 800)
screen.bgcolor("black")
turtle.colormode(255)

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.pensize(1)

# 성능: 수동 업데이트 (빠르게 그리기)
screen.tracer(0, 0)

def rand_color():
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

# 1) 리사주 곡선 (Lissajous)
def draw_lissajous(A=300, B=300, a=3, b=2, delta=math.pi/2, steps=2000):
    t.pensize(2)
    t.penup()
    for i in range(steps):
        theta = 2 * math.pi * i / steps
        x = A * math.sin(a * theta + delta)
        y = B * math.sin(b * theta)
        if i == 0:
            t.goto(x, y)
            t.pendown()
            t.pencolor(rand_color())
        else:
            if i % 200 == 0:  # 색 변환
                t.pencolor(rand_color())
            t.goto(x, y)
    screen.update()

# 2) 슈퍼 스파이로그래프 (Hypotrochoid / Spirograph)
def draw_spiro(R=150, r=60, d=80, steps=5000):
    t.penup()
    t.pensize(1)
    t.pencolor(rand_color())
    for i in range(steps):
        theta = 2 * math.pi * i / steps
        # hypotrochoid param
        x = (R - r) * math.cos(theta) + d * math.cos(((R - r) / r) * theta)
        y = (R - r) * math.sin(theta) - d * math.sin(((R - r) / r) * theta)
        if i == 0:
            t.goto(x, y)
            t.pendown()
        else:
            if i % 400 == 0:
                t.pencolor(rand_color())
            t.goto(x, y)
    screen.update()

# 3) 버터플라이 커브 (Butterfly curve)
def draw_butterfly(steps=2000, scale=60):
    t.penup()
    for i in range(steps):
        tval = i * 12 * math.pi / steps  # 0..12π
        # 유명한 butterfly 식 (parametric)
        r = math.e**(math.cos(tval)) - 2*math.cos(4*tval) - (math.sin(tval/12))**5
        x = scale * math.sin(tval) * r
        y = scale * math.cos(tval) * r
        if i == 0:
            t.goto(x, y)
            t.pendown()
            t.pencolor(rand_color())
        else:
            if i % 200 == 0:
                t.pencolor(rand_color())
            t.goto(x, y)
    screen.update()

# 4) 시어핀스키 삼각형 (Chaos game)
def draw_sierpinski(iterations=40000, size=400):
    # 삼각형 꼭짓점
    v1 = (-size//2, -size//3)
    v2 = (size//2, -size//3)
    v3 = (0, size//2)
    t.penup()
    # 시작점
    x, y = 0, 0
    t.goto(x, y)
    for i in range(iterations):
        vx = random.choice([v1, v2, v3])
        x = (x + vx[0]) / 2
        y = (y + vx[1]) / 2
        # 점 찍기
        t.goto(x, y)
        t.dot(2, rand_color() if i % 500 == 0 else (255,255,255))
        if i % 1000 == 0:
            screen.update()
    screen.update()

# 5) 코흐 눈송이 (Koch snowflake, 재귀)
def koch(turtle_obj, order, size):
    if order == 0:
        turtle_obj.forward(size)
    else:
        koch(turtle_obj, order-1, size/3)
        turtle_obj.left(60)
        koch(turtle_obj, order-1, size/3)
        turtle_obj.right(120)
        koch(turtle_obj, order-1, size/3)
        turtle_obj.left(60)
        koch(turtle_obj, order-1, size/3)

def draw_koch_snowflake(order=3, size=400):
    t.penup()
    t.goto(-size/2, size/6)
    t.pendown()
    t.pencolor(rand_color())
    for _ in range(3):
        koch(t, order, size)
        t.right(120)
    screen.update()

# 6) 페인트 효과: 여러 모양 랜덤 배치
def draw_random_show():
    funcs = [draw_lissajous, draw_spiro, draw_butterfly, lambda: draw_koch_snowflake(3, 300), lambda: draw_sierpinski(30000, 300)]
    random.shuffle(funcs)
    for f in funcs:
        t.clear()
        f()
        time.sleep(0.6)
    screen.update()

# 인터페이스
menu = """원하는 모양의 번호를 입력하세요:
1 - Lissajous 곡선 (아름다운 라인)
2 - Spirograph (스파이로그래프, 가변 패턴)
3 - Butterfly curve (버터플라이)
4 - Sierpinski 삼각형 (프랙탈, chaos game)
5 - Koch Snowflake (코흐 눈송이)
6 - 랜덤 쇼 (여러 모양 자동 재생)
0 - 모두 지우기 / 다시 시작
입력: """

choice = screen.textinput("수학적 모양", menu)

# 안전: 텍스트 입력이 None이면 종료
if choice is None:
    turtle.bye()
else:
    t.clear()
    if choice == "1":
        draw_lissajous()
    elif choice == "2":
        draw_spiro()
    elif choice == "3":
        draw_butterfly()
    elif choice == "4":
        draw_sierpinski()
    elif choice == "5":
        draw_koch_snowflake(order=4, size=500)
    elif choice == "6":
        draw_random_show()
    elif choice == "0":
        t.clear()
        screen.update()
    else:
        # 숫자 외 입력이면 간단히 랜덤 하나 실행
        draw_random_show()

# 끝낼 때 클릭 기다리기
screen.tracer(1, 10)
turtle.done()
