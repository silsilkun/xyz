import turtle
import random
import time
import os

# --------- 설정 ----------
screen = turtle.Screen()
screen.title("마우스 드로잉 - 왼쪽 드래그로 그림 그리기")
screen.setup(1000, 700)
screen.bgcolor("white")
turtle.colormode(255)

drawer = turtle.Turtle()
drawer.hideturtle()
drawer.speed(0)
drawer.penup()

# 상태 저장: 현재 색/두께, 그리고 드래그 하나를 하나의 "stroke"로 저장해 undo 가능하게 함
current_color = (0, 0, 0)
pen_size = 3
strokes = []  # 각 stroke는 turtle.RawTurtle의 stamp id 리스트 대신 'paths'로 저장 (post facto undo by clearing and redrawing)
# simpler approach: keep a list of paths where each path = [(x,y), ...], plus its color and size

paths = []  # list of dicts: {"points": [(x,y),...], "color":(r,g,b), "size":n}
current_path = None
is_drawing = False

# ---------- 헬퍼 ----------
def rand_color():
    return (random.randint(20, 240), random.randint(20, 240), random.randint(20, 240))

def redraw_all():
    """모든 저장된 경로를 지우고 다시 그린다 (undo 또는 clear 이후 재렌더용)"""
    drawer.clear()
    drawer.penup()
    for p in paths:
        drawer.pencolor(p["color"])
        drawer.pensize(p["size"])
        pts = p["points"]
        if not pts:
            continue
        drawer.goto(pts[0])
        drawer.pendown()
        for xy in pts[1:]:
            drawer.goto(xy)
        drawer.penup()
    screen.update()

# ---------- 마우스 이벤트 핸들러 ----------
def start_draw(x, y):
    global is_drawing, current_path
    is_drawing = True
    current_path = {"points": [(x,y)], "color": current_color, "size": pen_size}
    # 바로 시각화
    drawer.pencolor(current_color)
    drawer.pensize(pen_size)
    drawer.penup()
    drawer.goto(x, y)
    drawer.pendown()

def draw_move(x, y):
    global current_path
    if not is_drawing:
        return
    # 추가 포인트
    current_path["points"].append((x, y))
    drawer.goto(x, y)

def end_draw(x, y):
    global is_drawing, current_path
    if not is_drawing:
        return
    # 마무리
    current_path["points"].append((x, y))
    paths.append(current_path)
    current_path = None
    is_drawing = False
    drawer.penup()

# 오른쪽 클릭: 랜덤 색으로 변경
def right_click_handler(x, y):
    global current_color
    current_color = rand_color()
    # 짧은 피드백: 포인터 색 바꾸기 (임시)
    drawer.penup()
    drawer.goto(x, y)
    drawer.dot(8, current_color)

# ---------- 마우스 휠 바인딩 (윈도우/맥/Tk 호환 처리) ----------
def on_mouse_wheel(event):
    # Windows: event.delta (120 단위), Mac may be smaller; Linux might use Button-4/5
    global pen_size
    delta = 0
    if hasattr(event, "delta") and event.delta != 0:
        delta = event.delta
    elif event.num == 4:  # Linux wheel up
        delta = 120
    elif event.num == 5:  # Linux wheel down
        delta = -120

    if delta > 0:
        pen_size = min(50, pen_size + 1)
    else:
        pen_size = max(1, pen_size - 1)
    # 간단한 HUD: 찍어주기
    drawer.penup()
    drawer.goto(-480, 320)
    drawer.clear()
    # We will not clear the whole drawing; instead we redraw HUD by using a temporary turtle.
    # To keep simple, call redraw_all which will re-render drawing (and then draw HUD)
    redraw_all()
    # draw HUD text (using screen.title is easiest)
    screen.title(f"마우스 드로잉 - 펜 굵기: {pen_size}  색: {current_color}")

# ---------- 키 바인딩 ----------
def clear_all():
    global paths
    paths = []
    drawer.clear()
    screen.title("마우스 드로잉 - 캔버스가 지워졌습니다.")

def save_canvas():
    """캔버스를 PostScript로 저장 (다른 형식은 외부 라이브러리 필요)"""
    timestr = time.strftime("%Y%m%d_%H%M%S")
    filename = f"drawing_{timestr}.ps"
    # Tkinter Canvas를 통해 postscript로 저장
    canvas = screen.getcanvas()
    try:
        canvas.postscript(file=filename)
        screen.title(f"저장됨: {os.path.abspath(filename)}")
    except Exception as e:
        screen.title(f"저장 실패: {e}")

def set_pen_size_1_to_9(n):
    global pen_size
    pen_size = n
    screen.title(f"펜 굵기 설정: {pen_size}")

def undo_last():
    if not paths:
        return
    paths.pop()
    redraw_all()

# ---------- 바인딩 적용 ----------
# left mouse: press -> start, drag -> draw_move, release -> end
screen.onclick(start_draw, btn=1, add=True)
# For continuous drawing when moving with left button pressed, use getcanvas().bind to <B1-Motion>
screen.getcanvas().bind("<B1-Motion>", lambda e: draw_move(turtle.Turtle().screen.cv.canvasx(e.x), turtle.Turtle().screen.cv.canvasy(e.y)) if False else draw_move(screen.cv.canvasx(e.x), screen.cv.canvasy(e.y)) )

# But the above lambda is messy; better use canvas coords translated to turtle coords:
def _motion_event(e):
    # e.x, e.y are canvas coordinates (origin top-left). Convert to turtle coords (origin center, y up).
    canvas = screen.getcanvas()
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    tx = e.x - w/2
    ty = h/2 - e.y
    draw_move(tx, ty)

screen.getcanvas().bind("<B1-Motion>", _motion_event)
# left release
screen.getcanvas().bind("<ButtonRelease-1>", lambda e: end_draw(*(_canvas_to_turtle(e))))

# right click
def _right_event(e):
    canvas = screen.getcanvas()
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    tx = e.x - w/2
    ty = h/2 - e.y
    right_click_handler(tx, ty)
screen.getcanvas().bind("<Button-3>", _right_event)

# wheel (Windows / Mac)
def _wheel_event(e):
    on_mouse_wheel(e)
# bind common wheel events
screen.getcanvas().bind("<MouseWheel>", _wheel_event)   # Windows, Mac (may have delta)
screen.getcanvas().bind("<Button-4>", _wheel_event)     # some Linux
screen.getcanvas().bind("<Button-5>", _wheel_event)

# helper to convert canvas event coords to turtle coords for release
def _canvas_to_turtle(e):
    canvas = screen.getcanvas()
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    tx = e.x - w/2
    ty = h/2 - e.y
    return (tx, ty)

# key bindings via screen.onkey
screen.listen()
screen.onkey(clear_all, "c")
screen.onkey(save_canvas, "s")
screen.onkey(undo_last, "u")
# 숫자 1~9로 굵기 설정
for i in range(1, 10):
    screen.onkey(lambda n=i: set_pen_size_1_to_9(n), str(i))

# 화면 초기 HUD
screen.title("마우스 드로잉 - 왼쪽 드래그로 그림, 오른쪽 클릭 색 변경, c:clear s:save u:undo 1-9:pen size")

# Ensure turtle canvas reference for coordinate conversion
# some environments require access to internal canvas; attach for convenience
try:
    screen.cv = screen.getcanvas()
except Exception:
    pass

# keep window open
turtle.mainloop()
