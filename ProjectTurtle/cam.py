import cv2
import turtle

# ---------- 카메라에서 사진 찍기 ----------
cap = cv2.VideoCapture(0)  # 0: 기본 웹캠
if not cap.isOpened():
    raise Exception("카메라를 열 수 없습니다.")

print("스페이스바를 눌러 사진을 찍으세요.")

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 32:  # 스페이스바
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        break
    elif key == 27:  # ESC 종료
        cap.release()
        cv2.destroyAllWindows()
        exit()

cap.release()
cv2.destroyAllWindows()

# ---------- 윤곽선 추출 ----------
edges = cv2.Canny(img, 100, 200)
contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# ---------- Turtle 세팅 ----------    
screen = turtle.Screen()
screen.setup(900, 700)
screen.bgcolor("white")
t = turtle.Turtle()
t.speed(0)
t.hideturtle()
t.pensize(1)
t.pencolor("black")
t.penup()

# ---------- 중앙 정렬 + 스케일 ----------
screen_width = 800
screen_height = 600
img_h, img_w = img.shape

scale_x = screen_width / img_w * 0.9
scale_y = screen_height / img_h * 0.9
scale = min(scale_x, scale_y)

offset_x = -img_w*scale/2
offset_y = img_h*scale/2

# ---------- 윤곽선 그리기 ----------
step = 5  # 점 건너뛰기
for contour in contours:
    last_pos = None
    for i in range(0, len(contour), step):
        x, y = contour[i][0]
        tx = x*scale + offset_x
        ty = -y*scale + offset_y

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
