import cv2

image = cv2.imread('C:/aurorealis/420lab/imgs/plan.jpg')
image = cv2.resize(image, (0, 0), fx=0.7, fy=0.7)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

template= cv2.imread('C:/aurorealis/420lab/imgs/balcony.jpg', 0)
template = cv2.resize(template, (0, 0), fx=0.7, fy=0.7)

flat_dict = {}
#balcony
flat_dict["на балконе"] = (231, 92, 458, 192)
image = cv2.rectangle(image, (231, 92), (458, 192), (0, 255, 255), 3)
#kitchen
flat_dict["на кухне"] = (239, 194, 447,  372)
image = cv2.rectangle(image, (239, 194), (447,  372), (0, 0, 255), 3)
#bathroom
flat_dict["в ванной"] = (317,  371, 447, 484)
image = cv2.rectangle(image, (317,  371), (447, 484), (255, 0, 0), 3)
#hall
flat_dict["в холле"] = (240, 485 , 445, 610)
image = cv2.rectangle(image, (240, 485), ( 445, 610), (255 ,0, 255), 3)
#entry
flat_dict["в прихожей"] = (118, 499, 233, 613)
image = cv2.rectangle(image, (118, 499), (233, 613), (255 , 255, 0), 3)
#room
flat_dict["в комнате"] = (451, 261, 663,  614)
image = cv2.rectangle(image, (451, 261), (663,  614), (0 , 255, 0), 3)

result= cv2.matchTemplate(gray, template, cv2.TM_SQDIFF)
min_val, max_val, min_loc, max_loc= cv2.minMaxLoc(result)
height, width= template.shape[:2]
top_left= min_loc
center= (top_left[0] + int(width/2), top_left[1] + int(height/2))
#cv2.rectangle(image, top_left, bottom_right, (0,0,255),5)

out_text = ""
for key, value in flat_dict.items():
    if (value[0] < center[0]) and (center[0] < value[2]) and (value[1] < center[1]) and (center[1] < value[3]):
        out_text = ("Ты " + key)

if out_text:
    print(out_text)
else:
    print("Ты не в квартире")

#cv2.imshow('Result', image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()