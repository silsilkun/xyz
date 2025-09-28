import turtle
import time

# ---------- 화면 세팅 ----------
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Interactive Waves")
turtle.tracer(0)

waves = []

# ---------- 파동 클래스 ----------
class Wave:
    def __init__(self, x, y, radius=10, max_radius=200, color_val=255):
        self.x = x
        self.y = y
        self.radius = radius
        self.max_radius = max_radius
        self.color_val = color_val
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.speed(0)

    def draw(self):
        self.t.clear()
        if self.radius > self.max_radius or self.color_val <= 0:
            return False
        hex_color = "#{:02x}{:02x}{:02x}".format(self.color_val, self.color_val, self.color_val)
        self.t.pencolor(hex_color)
        self.t.penup()
        self.t.goto(self.x, self.y - self.radius)
        self.t.pendown()
        self.t.circle(self.radius)
        self.radius += 5
        self.color_val = max(0, self.color_val - 5)  # 점점 어둡게
        return True

# ---------- 애니메이션 루프 ----------
def update():
    alive_waves = []
    for wave in waves:
        if wave.draw():
            alive_waves.append(wave)
    waves[:] = alive_waves
    turtle.update()
    screen.ontimer(update, 50)

# ---------- 클릭 시간 기반 ----------
press_time = None
press_pos = (0, 0)

def on_press(event):
    global press_time, press_pos
    press_time = time.time()
    press_pos = (event.x - screen.window_width()//2, screen.window_height()//2 - event.y)
    # 눌렀을 때 바로 파동 생성
    waves.append(Wave(press_pos[0], press_pos[1]))

def on_release(event):
    global press_time
    if press_time is None:
        return
    duration = time.time() - press_time
    num_waves = max(1, int(duration * 5))  # 1초 누르면 5개 파동
    for i in range(num_waves):
        waves.append(Wave(press_pos[0], press_pos[1], radius=10 + i*10))
    press_time = None

# ---------- 드래그 이벤트 ----------
def on_drag(event):
    x = event.x - screen.window_width()//2
    y = screen.window_height()//2 - event.y
    waves.append(Wave(x, y))

# ---------- Tkinter 이벤트 연결 ----------
canvas = screen.getcanvas()
canvas.bind("<ButtonPress-1>", on_press)
canvas.bind("<ButtonRelease-1>", on_release)
canvas.bind("<B1-Motion>", on_drag)

update()
screen.mainloop()
