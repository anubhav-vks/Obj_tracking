import cv2 as cv
from cv2 import aruco
import numpy as np

marker_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
# print(marker_dict)
param_markers = aruco.DetectorParameters()
# print(param_markers)
detector = cv.aruco.ArucoDetector(marker_dict, param_markers)
# print(detector)
cap = cv.VideoCapture(0)

# select the id of the tracker we want
id = 8

while True:
    ret, frame = cap.read()
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = detector.detectMarkers(gray_frame)
    if marker_corners:
        for ids, corners in zip(marker_IDs, marker_corners):
            if ids == id:
                # print(corners)
                corners = corners.reshape(4, 2)
                # print(corners)
                corners = corners.astype(int) # float to int
                # print(corners)
                top_right = corners[0]
                top_left = corners[1]
                bottom_right = corners[2]
                bottom_left = corners[3]
                # print(top_right)
                center_x = int((top_right[0] + top_left[0] + bottom_left[0] + bottom_right[0])/4)
                center_y = int((bottom_left[1] + bottom_right[1] + top_left[1]+ top_right[1]) /4)
                # print(center_x, center_y)
                cv.putText(frame,f"{center_x, center_y}",(center_x, center_y),cv.FONT_HERSHEY_PLAIN,1.3,(200, 100, 0),2,cv.LINE_AA,)
                # print(ids, "  ", corners)
    cv.imshow("frame", frame)
    key = cv.waitKey(1)
    if key == ord("q"):
        break
cap.release()
cv.destroyAllWindows()