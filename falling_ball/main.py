import cv2
import numpy as np
import numpy as np
import pygame
import pygame.gfxdraw
import pygame as pg
from random import randrange
import pymunk.pygame_util



def lower_update(value):
    global lower
    lower = value


def upper_update(value):
    global upper
    upper = value


def find_paper_and_crop(thres):
    global pp_rect, pp_dst, maxW, maxH

    contours, _ = cv2.findContours(thres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_contour = max(contours, key=cv2.contourArea)

    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)

    if len(approx) == 4:
        pts = approx.reshape(4, 2)
        rect = order_points(pts)
        (tl, tr, br, bl) = rect

        # print("Ordered points:", rect)
        widthA = np.linalg.norm(br - bl)
        widthB = np.linalg.norm(tr - tl)
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.linalg.norm(tr - br)
        heightB = np.linalg.norm(tl - bl)
        maxHeight = max(int(heightA), int(heightB))

        dst = np.array(
            [
                [0, 0],
                [maxWidth, 0],
                [maxWidth, maxHeight],
                [0, maxHeight],
            ],
            dtype="float32",
        )
        pp_rect = rect
        pp_dst = dst
        maxW = maxWidth
        maxH = maxHeight
        warped = apply_perspective(thres, rect, dst, maxW, maxH)
        return warped
    else:
        raise Exception("Paper not detected or the paper does not have four corners")


def apply_perspective(image, rect, ppd, maxW, maxH):
    M = cv2.getPerspectiveTransform(rect, ppd)
    return cv2.warpPerspective(image, M, (maxW, maxH))

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def process_image(img):
    global pp_rect, pp_dst, maxW, maxH
    img = apply_perspective(img, pp_rect, pp_dst, maxW, maxH)
    img = cv2.resize(
        img,
        (0, 0),
        fx=1280 / img.shape[1],
        fy=800 / img.shape[0],
        interpolation=cv2.INTER_NEAREST_EXACT,
    )
    return img


def create_ball(space):
    ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    ball_body = pymunk.Body(ball_mass, ball_moment)
    ball_body.position = 500, 100
    ball_shape = pymunk.Circle(ball_body, ball_radius)
    ball_shape.elasticity = 1
    ball_shape.friction = 1
    space.add(ball_body, ball_shape)
    return ball_body


def create_segment(from_, to_, thickness, space, color):
    segment_shape = pymunk.Segment(space.static_body, from_, to_, thickness)
    segment_shape.color = pg.color.THECOLORS[color]
    space.add(segment_shape)


def create_rect(x1, y1, x2, y2, x3, y3, x4, y4):
    # правый верх, левый верх, левый низ, левый верх
    color = "green"
    create_segment((x1, y1), (x2, y2), 3, space, color )
    create_segment((x2, y2), (x3, y3), 3, space, color )
    create_segment((x3, y3), (x4, y4), 3, space, color )
    create_segment((x4, y4), (x1, y1), 3, space, color )



pymunk.pygame_util.positive_y_is_up = False

# cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_GUI_NORMAL)

# cap = cv2.VideoCapture(2)
# cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
# cap.set(cv2.CAP_PROP_EXPOSURE, 5)

lower = 0
upper = 55

cv2.createTrackbar("Lower", "Mask", lower, 255, lower_update)
cv2.createTrackbar("Upper", "Mask", upper, 255, upper_update)

pp_rect = []
pp_dst = []
maxW = 0
maxH = 0

# img = cap.read()[1]
img = cv2.imread("cllean.jpg")

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img = cv2.threshold(img, 10, 255, type=cv2.THRESH_BINARY)[1]
img = cv2.threshold(img, 10, 255, type=cv2.THRESH_BINARY)[1]

cv2.imshow("b", img)

# while True: cv2.waitKey(1)

crop = find_paper_and_crop(img)
# cv2.imshow("a", crop)

crop = cv2.resize(
    crop,
    (0, 0),
    fx=1280 / crop.shape[1],
    fy=800 / crop.shape[0],
    interpolation=cv2.INTER_NEAREST_EXACT,
)

RES = WIDTH, HEIGHT = 1280, 800
FPS = 60

surface = pg.display.set_mode((0, 0), pygame.FULLSCREEN, display=1)

# print(pg.display.get_desktop_sizes())
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

space = pymunk.Space()
space.gravity = 0, 1000
ball_mass, ball_radius = 1000000, 10

balls = [([randrange(256) for i in range(3)], create_ball(space)) for j in range(0)]

while True:
    #     bts = socket.recv()

    surface.fill(pg.Color("white"))

    space.step(1 / FPS)
    space.debug_draw(draw_options)
    for color, ball in balls:
        if (
            ball.position.x < -ball_radius
            or ball.position.x > WIDTH + ball_radius
            or ball.position.y < -ball_radius
            or ball.position.y > HEIGHT + ball_radius
        ):
            ball.position = 500, 100
            ball.velocity = (0, 0)

    pg.display.flip()
    clock.tick(FPS)

    # cv2.imshow("Image", frame2)
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            space.remove(*space.shapes)
            balls = [([randrange(256) for i in range(3)], create_ball(space)) for j in range(100)]

            # aeae = cap.read()[1]
            aeae = cv2.imread("cllean.jpg")

            aeae = process_image(aeae)
            # frame = aeae.copy()
            # frame2 = frame.copy()
            gray = aeae.copy()
            #         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7, 7), 0)
            mask = cv2.Canny(gray, lower, upper)
            # cv2.imshow('Mask', mask)
            cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)          
            # for i in range(len(cnts)):
            #     cv2.drawContours(frame2, cnts, i, (0, 0, 0), 1)
            for index, cnt in enumerate(cnts):
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                # cv2.drawContours(frame2, [box], 0, (0, 0, 255), 2)
                create_rect(*[a for b in box for a in b])

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            cv2.destroyAllWindows()
            exit()