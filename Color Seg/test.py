import requests 
import cv2 
import numpy as np 
import imutils 
url = "http://192.168.1.33:8080/shot.jpg"
def setValues(x):
    print("")
      
#For Hsv Window Trackbar
cv2.namedWindow("Color detectors")
cv2.resizeWindow("Color detectors", width=680, height=280)
cv2.createTrackbar("Upper Hue", "Color detectors", 21,180, setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors", 255,255, setValues)
cv2.createTrackbar("Upper Value", "Color detectors", 255,255, setValues)
cv2.createTrackbar("Lower Hue", "Color detectors", 0,180, setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors", 208,255, setValues)
cv2.createTrackbar("Lower Value", "Color detectors", 160,255, setValues)
global roi

while True:
    img_resp = requests.get(url) 
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8) 
    img = cv2.imdecode(img_arr, -1) 
    img = imutils.resize(img, width=500, height=900) 
    # cv2.imshow("Android_cam", img) 
    
    roi = cv2.selectROI(img)
    print(roi)
    break

# Loop for every frame in video
while True: 
    # Take frame input from the Android phone cam
    img_resp = requests.get(url) 
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8) 
    img = cv2.imdecode(img_arr, -1) 
    img = imutils.resize(img, width=500, height=900) 
    cv2.imshow("Android_cam", img) 
    
    frame = img[int(roi[1]):int(roi[1]+roi[3]),
                int(roi[0]):int(roi[0] + roi[2])] 
    
    # frame = img
    img1 = img
    # Take HSV value from user
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
    u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
    u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")
    l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
    l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
    l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")

    Upper_hsv = np.array([u_hue, u_saturation,u_value])
    Lower_hsv = np.array([l_hue, l_saturation, l_value])
        
    mask = cv2.inRange(hsv, Lower_hsv,Upper_hsv)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    res = cv2.medianBlur(res, 5)
    # cv2.imshow("original image", frame)
    cv2.imshow('masked img', res)
    canny_out = cv2.Canny(res, 80, 120)
    #threshold (if 80 then 120)
    
    #Contours are for edge detection 
    contours, _ = cv2.findContours(canny_out, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # moments tell the easy matrix for edges (for memory optimisation, like only 4 points save for square and not the whole image matrix)
    moments = cv2.moments(canny_out)
        
    if moments['m00'] != 0:
        centroid_x = int(moments['m10'] / moments['m00'])
        centroid_y = int(moments['m01'] / moments['m00'])
    else:
           # Set values as zero
        centroid_x, centroid_y = 0, 0
    out = canny_out
    centro = str(centroid_x) +" , " +str(centroid_y)
    # cv2.circle(out, center=(centroid_x, centroid_y), radius=5,color= (255, 0, 0),thickness= -1)
    # cv2.putText(out, centro, (centroid_x, centroid_y), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1 )
    cv2.imshow('CANNY', out)
        
    # c = cv2.waitKey(5)
    # if c==27:
    #     break
    
    # Esc key to exit 
    if cv2.waitKey(1) == 27: 
        break
  
cv2.destroyAllWindows() 

