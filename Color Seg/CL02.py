import requests
import cv2
import numpy as np
import imutils

# URL for capturing the image
url = "http://192.168.1.33:8080/shot.jpg"

def set_values(x):
    pass

def create_color_detector_window():
    cv2.namedWindow("Color Detectors")
    cv2.resizeWindow("Color Detectors", 680, 280)
    cv2.createTrackbar("Upper Hue", "Color Detectors", 21, 180, set_values)
    cv2.createTrackbar("Upper Saturation", "Color Detectors", 255, 255, set_values)
    cv2.createTrackbar("Upper Value", "Color Detectors", 255, 255, set_values)
    cv2.createTrackbar("Lower Hue", "Color Detectors", 0, 180, set_values)
    cv2.createTrackbar("Lower Saturation", "Color Detectors", 208, 255, set_values)
    cv2.createTrackbar("Lower Value", "Color Detectors", 160, 255, set_values)

def get_image(url):
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = imutils.resize(img, width=500, height=900)
    return img

def main():
    create_color_detector_window()
    global roi

    # Select ROI 
    while True:
        img = get_image(url)
        cv2.imshow("Android_cam", img)
        roi = cv2.selectROI("Android_cam", img)
        print(roi)
        break

    while True:
        img = get_image(url)
        cv2.rectangle(img, (int(roi[0]), int(roi[1])), (int(roi[0] + roi[2]), int(roi[1] + roi[3])), (255, 0, 0), 2)
        cv2.imshow("Android_cam", img)

        frame = np.zeros(img.shape, dtype=np.uint8)
        frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])] = img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

        hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        u_hue = cv2.getTrackbarPos("Upper Hue", "Color Detectors")
        u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color Detectors")
        u_value = cv2.getTrackbarPos("Upper Value", "Color Detectors")
        l_hue = cv2.getTrackbarPos("Lower Hue", "Color Detectors")
        l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color Detectors")
        l_value = cv2.getTrackbarPos("Lower Value", "Color Detectors")

        upper_hsv = np.array([u_hue, u_saturation, u_value])
        lower_hsv = np.array([l_hue, l_saturation, l_value])

        mask = cv2.inRange(hsv_img, lower_hsv, upper_hsv)
        # cv2.imshow("nw", mask)
        res = cv2.bitwise_and(frame, frame, mask=mask)  # Bitwise_AND b/w the image and itself but only in the region of mask
        res = cv2.medianBlur(res, 5)

        cv2.imshow('Masked Image', res)

        canny_out = cv2.Canny(res, 80, 120)
        contours, hierarchy = cv2.findContours(canny_out, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # moments are data types to store easy representation of contours like save only 2 points for a rectangle
        moments = cv2.moments(canny_out)
        if moments['m00'] != 0:
            centroid_x = int(moments['m10'] / moments['m00'])
            centroid_y = int(moments['m01'] / moments['m00'])
        else:
            centroid_x, centroid_y = 0, 0

        cv2.circle(canny_out, (centroid_x, centroid_y), 5, (255, 0, 0), -1)
        cv2.putText(canny_out, f"{centroid_x}, {centroid_y}", (centroid_x, centroid_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
        cv2.imshow('Canny Output', canny_out)

        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
