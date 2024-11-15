from ultralytics import YOLO

model = YOLO("det_model/yolo11n.pt")
model.export(format='onnx')
print("DONE")