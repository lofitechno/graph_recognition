import cv2

image= cv2.imread('C:/aurorealis/420lab/imgs/plan.jpg')
image = cv2.resize(image, (0, 0), fx=0.7, fy=0.7)
gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

template= cv2.imread('C:/aurorealis/420lab/imgs/room.jpg', 0)
template = cv2.resize(template, (0, 0), fx=0.7, fy=0.7)

result= cv2.matchTemplate(gray, template, cv2.TM_SQDIFF)
min_val, max_val, min_loc, max_loc= cv2.minMaxLoc(result)
height, width= template.shape[:2]
top_left= min_loc
bottom_right= (top_left[0] + width, top_left[1] + height)
cv2.rectangle(image, top_left, bottom_right, (0,0,255),5)
cv2.imshow('Result', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
