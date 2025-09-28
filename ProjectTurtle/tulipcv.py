import cv2
import turtle

# 이미지 불러오기
img = cv2.imread("tulip.jpg", 0)
if img is None:
    raise FileNotFoundError("tulip3.jpg 파일이 필요합니다.")

# 윤곽선 추출
edges = cv2.Canny(img, 100, 200)
contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# Turtle 세팅
screen = turtle.Screen()
screen.bgcolor("white")
t = turtle.Turtle()
t.speed(0)
t.hideturtle()
t.pensize(2)
t.penup()

# 자동 중앙 정렬 + 최대 크기 스케일
# 화면 기준 최대 크기
screen_width = 800
screen_height = 600
img_h, img_w = img.shape

scale_x = screen_width / img_w * 0.9   # 0.9: 화면 여유
scale_y = screen_height / img_h * 0.9
scale = min(scale_x, scale_y)

offset_x = -img_w*scale/2
offset_y = img_h*scale/2

# 윤곽선 그리기
step = 5  # 점 건너뛰기
for contour in contours:
    last_pos = None
    for i in range(0, len(contour), step):
        x, y = contour[i][0]
        tx = x*scale + offset_x
        ty = -y*scale + offset_y

        # 중복 좌표 제거
        if last_pos is not None:
            dx = abs(tx - last_pos[0])
            dy = abs(ty - last_pos[1])
            if dx < 1 and dy < 1:
                continue

        if i == 0:
            t.penup()
            t.goto(tx, ty)
            t.pendown()
        else:
            t.goto(tx, ty)

        last_pos = (tx, ty)

turtle.done()
