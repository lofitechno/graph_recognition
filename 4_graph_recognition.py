import cv2
import numpy as np
import random as rng
import math
import pytesseract
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Вспомогательная функция для расчета расстояний
def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

# считываем изображение
image = cv2.imread('C:/aurorealis/420lab/imgs/graph4.jpg')
scale = 0.2  # масштаб
original = cv2.resize(image, (0, 0), fx=scale, fy=scale) #картинка для вспомогательной отрисовки

#Копия изображения для предобработки
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.resize(gray, (0, 0), fx=scale, fy=scale)

#находим узлы преобразованиями Хафа
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
                           param1=50, param2=30, minRadius=20, maxRadius=100)
#если нашёлся хотя бы один круг - рисуем
node_centers = []
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    # рисуем круги и их центры
    for (x, y, r) in circles:
        # цвет рандомный - это важно
        color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        # при отрисовке радиус * 2
        cv2.circle(original, (x, y), 2 * r, color, -1)
        cv2.rectangle(original, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        node_centers.append((x, y, color))

#Теперь переходим к надписям
img = image
img = cv2.resize(img, (0, 0), fx=0.2, fy=0.2)
ret, img = cv2.threshold(img, 137, 255, cv2.THRESH_BINARY)
# немного морфологии
kernel = np.ones((2, 2), 'uint8')
img = cv2.dilate(img, kernel, iterations=2)
img = cv2.erode(img, kernel, iterations=1)
# находим надписи
d = pytesseract.image_to_data(img, output_type=Output.DICT)
n_boxes = len(d['level'])
# рисуем ббоксы
bbox_centers = []
for i in range(n_boxes):
    if (len(d['text'][i]) > 2):  # != ""):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        cv2.rectangle(original, (x, y), (x + w, y + h), (0, 255, 0), 2)
        bbox_centers.append((x + int(w / 2), y + int(h / 2), d['text'][i]))

#сопоставляем каждому узлу по надписи
named_nodes = {}
for bbox in bbox_centers:
    min = 10000
    for node in node_centers:
        #считаем расстояние от узла до налписи - наименьшее считаем за искомое
        distance = calculateDistance(bbox[0], bbox[1], node[0], node[1])
        node_name = ""
        if (distance < min):
            min = distance
            node_name = bbox[2]
            #node_center = (node[0], node[1])
        if(node_name != ""):
            named_nodes[node_name] = node
#print(named_nodes)

#находим рёбра графа
#копируем исходное изображение и предобрабатываем
img = image
img = cv2.resize(img, (0,0), fx=scale, fy=scale)
ret, img = cv2.threshold(img,130,255,cv2.THRESH_BINARY)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#Гауссово размытие
blur_gray = cv2.GaussianBlur(gray,(3, 3),0)
#детектор Кенни
edges = cv2.Canny(blur_gray, 130, 255)
#нахождение линий рёбер преобразованиями Хафа
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 15, np.array([]) ,100 , 5)
#следующие строки для отрисовки получившихся линий
'''
for x in range(0, len(lines)):
    for x1, y1, x2, y2 in lines[x]:
        cv2.line(original, (x1, y1), (x2, y2), (0, 255, 0), 2)
'''

'''
Найдём рёбра соответствующие каждому узлу
#мы итерируемся по парам  разных узлов и линиям, соответсвующим рёбрам
#узнаём цвета окружностей на концах рёбер(напомню они рандомные)
#если цвета на концах линий совпадают с цветами текущих итерируемых узлов -> записываем соответвие в словарь
'''
out = {}
for key1, value1 in named_nodes.items():
    connected_nodes = set()
    for key2, value2 in named_nodes.items():
        if (key1 != key2):
            for x in range(0, len(lines)):
                for x1, y1, x2, y2 in lines[x]:
                    if (((tuple(original[x1][y1]) == value1[2]) and (tuple(original[x2][y2]) == value2[2])) or \
                    ((tuple(original[x2][y2]) == value1[2]) and (tuple(original[x1][y1]) == value2[2]))):
                        connected_nodes.add(key2)
    out[key1] = list(connected_nodes)

#print(out)
cv2.imshow("sd", original)
cv2.waitKey(0)
