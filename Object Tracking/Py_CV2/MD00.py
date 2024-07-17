import numpy as np
import cv2
import imutils
import requests

def setValues(x):
    print("")

url = "http://192.168.1.33:8080/shot.jpg"
cv2.namedWindow("Threshold")
cv2.resizeWindow("Threshold", width=680, height=80)
cv2.createTrackbar("Lower Threshold", "Threshold", 0,500, setValues)
cv2.createTrackbar("Upper threshold", "Threshold", 0,550, setValues)

while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1) 
    img = imutils.resize(img, width=500, height=900) 
    cv2.imshow("Android_cam", img) 
    frame = img
    
    u = cv2.getTrackbarPos("Lower Threshold", "Threshold")
    u2 = cv2.getTrackbarPos("Upper threshold", "Threshold")
    
    canny_out = cv2.Canny(frame, u, u2)
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
    
    if cv2.waitKey(1) == 27: 
        break
  
cv2.destroyAllWindows() 
