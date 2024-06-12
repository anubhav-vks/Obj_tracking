import cv2
import numpy as np

# For phone back color : HSV: 72,153,204 ,,, 0, 76, 102



def setValues(x):
    print("")
    
cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue", "Color detectors", 0,180, setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors", 0,255, setValues)
cv2.createTrackbar("Upper Value", "Color detectors", 0,255, setValues)
cv2.createTrackbar("Lower Hue", "Color detectors", 0,180, setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors", 0,255, setValues)
cv2.createTrackbar("Lower Value", "Color detectors", 0,255, setValues)
 
# get frame from camera and resize it and pass forward
def get_frame(cap, scaling_factor):
    ret, frame = cap.read()
    frame = cv2.resize(frame,None,fx= scaling_factor,fy=scaling_factor, interpolation=cv2.INTER_AREA)
    return frame
    
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    scaling_factor = 0.9
    
    while True:
        frame = get_frame(cap, scaling_factor)
        
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
        cv2.imshow("original image", frame)
        cv2.imshow('new img', res)
        
        c = cv2.waitKey(5)
        if c==27:
            break
    cv2.destroyAllWindows()