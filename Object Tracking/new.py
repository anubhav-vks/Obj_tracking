from ultralytics import YOLO
import torch

# torch.cuda.get_device_name(0)
# torch.cuda.get_device_name(1)
def main():
    torch.cuda.set_device(0)


# Load YOLOv10n model from scratch
    model = YOLO("yolov8n-cls.pt")
    result = model("tryfile.jpg")
    

# Train the model
    # model.train(data="custom_data.yaml", epochs=100, imgsz=320, cache = 'disk', batch = -1, workers = 0, patience = 6)
if __name__ == '__main__':
    main()
