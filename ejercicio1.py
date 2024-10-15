import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('moneditas.JPEG')

modified_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
modified_img = cv2.medianBlur(modified_img, 7)
modified_img = cv2.GaussianBlur(modified_img, (5, 5), 0)
modified_img = cv2.threshold(modified_img, 0, 150, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]

plt.imshow(modified_img, cmap='gray')
plt.show()

circ = cv2.HoughCircles(
    modified_img,
    cv2.HOUGH_GRADIENT,
    1,
    150,
    param1=80,
    param2=15,
    minRadius=40,
    maxRadius=120
)

monedas = {
    .01: 1626,
    .02: 1875,
    .05: 2125,
    .1: 1975,
    .2: 2225,
    .5: 2425,
    1: 2325,
    2: 2575
}

def distance(circle, x, y):
    return np.sqrt((x - circle[0]) ** 2 + (y - circle[1]) ** 2)

def click_event(event, x, y, a, b):
    if event == cv2.EVENT_LBUTTONDOWN:
        x *= 2.5
        y *= 2.5
        for c in circ[0]:
            if distance(c, x, y) <= c[2]:
                count_money(c[2])
                return

def count_money(euro1radius):
    correlation = monedas[1] / euro1radius
    result = {
        .01: 0,
        .02: 0,
        .05: 0,
        .1: 0,
        .2: 0,
        .5: 0,
        1: 0,
        2: 0
    }
    for c in circ[0]:
        radius = c[2]
        moneda = min(monedas, key=lambda x:abs(monedas[x] - (correlation * radius)))
        result[moneda] += 1

    count_result(result)

def count_result(result):
    total_money = 0
    for k, v in result.items():
        if v > 0:
            print(f"Hay {v} monedas de {k}€")
            total_money += v * k * 100
    print(f"Hay {total_money / 100}€")

def draw_and_show(nimg):
    for det in circ[0]:
        x_coor, y_coor, det_radio = det
        cv2.circle(nimg, (int(x_coor), int(y_coor)),
                   int(det_radio), (0, 255, 0), 2)
    cv2.imshow('Monedas', cv2.resize(nimg, (0, 0), fx=0.4, fy=0.4))
    cv2.setMouseCallback('Monedas', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


draw_and_show(img)

