import turtle
import math
import random

# 공통 설정
screen = turtle.Screen()
screen.bgcolor("black")
t = turtle.Turtle()
t.speed(0)
turtle.colormode(255)

# 랜덤 색상 함수
def rand_color():
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

# 1. 스피로그래프
def spirograph():
    t.pensize(2)
    for i in range(100):
        t.pencolor(rand_color())
        t.circle(100)
        t.left(360 / 100)

# 2. 프랙탈 같은 별 패턴
def star_pattern():
    t.pensize(1)
    for i in range(200):
        t.pencolor(rand_color())
        t.forward(i * 2)
        t.left(144)

# 3. 나선형 곡선
def spiral():
    t.pensize(2)
    for i in range(200):
        t.pencolor(rand_color())
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
        t.pencolor(rand_color())
        t.goto(x, y)
        t.pendown()

# 메인 메뉴
def main():
    print("1: 스피로그래프")
    print("2: 별 패턴")
    print("3: 나선형")
    print("4: 로즈 곡선")
    choice = screen.textinput("선택", "1~4 중 하나를 입력하세요:")

    t.hideturtle()
    if choice == "1":
        spirograph()
    elif choice == "2":
        star_pattern()
    elif choice == "3":
        spiral()
    elif choice == "4":
        rose_curve()
    else:
        print("잘못된 선택입니다.")

    turtle.done()

main()
