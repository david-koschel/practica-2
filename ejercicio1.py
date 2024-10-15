import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('moneditas.JPEG')

def show_image(img): #remove
    plt.axis('off')
    plt.imshow(img, cmap='gray')
    plt.show()

gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
pimg = cv2.medianBlur(gris, 7)
show_image(pimg) #remove

contornos2, hierarchy2 = cv2.findContours(pimg,
    cv2.RETR_EXTERNAL ,
    cv2.CHAIN_APPROX_SIMPLE)

circ = cv2.HoughCircles(
    pimg,
    cv2.HOUGH_GRADIENT,
    1,
    40,
    param1=180,
    param2=35,
    minRadius=70,
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
    correlation = euro1radius / monedas[1]
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
        moneda = min(monedas, key=lambda x:abs(1 - (correlation * monedas[x] / radius)))
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
    cv2.imshow('Monedas', cv2.resize(nimg, tuple(int(ti / 2.5) for ti in img.shape[1::-1])))
    cv2.setMouseCallback('Monedas', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


draw_and_show(img)

