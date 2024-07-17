import cv2
import numpy as np

# img = cv2.imread("image.jpg")
# print(img.shape)
# ratio = img.shape[0]/img.shape[1]
# new_h = 512
# new_img = cv2.resize(img,(600,250))
# print(ratio)
# cv2.imshow("window", new_img)
# cv2.waitKey(0)

img = np.zeros((512, 512,3))
flag = False
def draw(event, x, y, flags, params):
    global flag    
    if event == 1:    
        # cv2.circle(img, center=(x,y), radius=5, color=(255,255,0), thickness=1)
        flag = True
        # cv2.rectangle(img, (x,y), (0,0), (0,255,0), -1)
    elif event == 0:
        if flag == True:
            cv2.circle(img, center=(x,y), radius=1, color=(255,255,0), thickness=-1)
    elif event == 4:
        flag = False
        
cv2.namedWindow(winname="window" )
cv2.setMouseCallback("window", draw)

while True:
    cv2.imshow("window", img)
    
    if cv2.waitKey(1) & 0xFF == ord('a'):
        break
    
cv2.destroyAllWindows()