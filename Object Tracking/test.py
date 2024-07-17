import cv2
from ultralytics import YOLO

# Load your trained model
model = YOLO("best.pt")

# Capture video from the camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Run YOLOv8 inference
    results = model(frame)

    # Display the results
    cv2.imshow('YOLOv8 Inference', results[0].plot())

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()