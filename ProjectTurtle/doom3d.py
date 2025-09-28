import turtle
import math

# ---------- 화면 설정 ----------
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Wireframe 3D Mini DOOM with Crosshair")
screen.setup(width=800, height=600)
t = turtle.Turtle()
t.hideturtle()
t.speed(0)
turtle.tracer(0)

# ---------- 맵 (0=빈공간, 1~n=벽 종류) ----------
MAP = [
    [1,1,2,2,2,1,1],
    [1,0,0,0,0,0,1],
    [1,0,3,0,3,0,1],
    [1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1]
]

CELL_SIZE = 1

# ---------- 플레이어 ----------
player_x, player_y = 3.5, 3.5
player_angle = 0
FOV = math.pi / 3
NUM_RAYS = 80
MAX_DEPTH = 8

# ---------- 벽 색상 ----------
WALL_COLORS = {
    1: "gray",
    2: "blue",
    3: "brown"
}

# ---------- Wireframe 그리기 ----------
def draw_line(x1, y1, x2, y2, color="white"):
    t.pencolor(color)
    t.penup()
    t.goto(x1, y1)
    t.pendown()
    t.goto(x2, y2)

# ---------- 화면 중앙 가늠좌 ----------
def draw_crosshair():
    t.pencolor("red")
    t.pensize(2)
    cx, cy = 0, 0
    # 수평선
    t.penup()
    t.goto(cx - 10, cy)
    t.pendown()
    t.goto(cx + 10, cy)
    # 수직선
    t.penup()
    t.goto(cx, cy - 10)
    t.pendown()
    t.goto(cx, cy + 10)
    t.penup()
    t.pensize(1)

# ---------- Raycasting ----------
def cast_rays():
    t.clear()
    screen_width = 800
    screen_height = 600
    scale = 300

    for ray in range(NUM_RAYS):
        ray_angle = player_angle - FOV/2 + (ray / NUM_RAYS) * FOV
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)
        for depth in range(MAX_DEPTH*10):
            depth /= 10
            x = player_x + cos_a * depth
            y = player_y + sin_a * depth
            map_x = int(x)
            map_y = int(y)
            if 0 <= map_y < len(MAP) and 0 <= map_x < len(MAP[0]):
                if MAP[map_y][map_x] != 0:
                    proj_height = scale / (depth + 0.0001)
                    x_screen = -screen_width/2 + ray*(screen_width/NUM_RAYS)
                    color = WALL_COLORS.get(MAP[map_y][map_x], "white")
                    draw_line(x_screen, -proj_height/2, x_screen, proj_height/2, color)
                    break

    draw_crosshair()
    turtle.update()

# ---------- 키 상태 저장 ----------
keys = {"w": False, "s": False, "a": False, "d": False}

def key_press(key):
    keys[key] = True

def key_release(key):
    keys[key] = False

# ---------- 매 프레임 이동/회전 ----------
def update():
    global player_x, player_y, player_angle
    speed = 0.1
    turn_speed = 0.05

    if keys["w"]:
        dx = math.cos(player_angle) * speed
        dy = math.sin(player_angle) * speed
        if MAP[int(player_y + dy)][int(player_x + dx)] == 0:
            player_x += dx
            player_y += dy
    if keys["s"]:
        dx = math.cos(player_angle) * speed
        dy = math.sin(player_angle) * speed
        if MAP[int(player_y - dy)][int(player_x - dx)] == 0:
            player_x -= dx
            player_y -= dy
    if keys["a"]:
        player_angle -= turn_speed
    if keys["d"]:
        player_angle += turn_speed

    cast_rays()
    screen.ontimer(update, 30)

# ---------- 키 연결 ----------
screen.listen()
screen.onkeypress(lambda: key_press("w"), "w")
screen.onkeyrelease(lambda: key_release("w"), "w")
screen.onkeypress(lambda: key_press("s"), "s")
screen.onkeyrelease(lambda: key_release("s"), "s")
screen.onkeypress(lambda: key_press("a"), "a")
screen.onkeyrelease(lambda: key_release("a"), "a")
screen.onkeypress(lambda: key_press("d"), "d")
screen.onkeyrelease(lambda: key_release("d"), "d")

# ---------- 초기 화면 ----------
cast_rays()
update()
screen.mainloop()
