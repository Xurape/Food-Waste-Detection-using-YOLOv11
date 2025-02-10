from ultralytics import YOLO
import torch


class YOLOModel:
    def __init__(self):
        self.model = self.load_model()

    def load_model(self):
        try:
            print("Loading YOLO model...")
            model = YOLO("server/yolo/weights/yolov11-x-weights-v6.pt")
            print("Model loaded!")
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            return None

    def predict(self, frame):
        try:
            print("Predicting...")
            with torch.no_grad():
                results = self.model(frame)
            detected_objects = []
            for result in results:
                for i, (mask, box) in enumerate(zip(result.masks.data, result.boxes)):
                    area = mask.sum().item()
                    detected_objects.append(
                        {
                            "label": box.cls.item(),
                            "label_name": result.names[box.cls.item()],
                            "confidence": box.conf.item(),
                            "box": box.xyxy.tolist(),
                            "area": area,
                        }
                    )

            print("Success!")
            return detected_objects, results
        except Exception as e:
            print(f"Error predicting: {e}")
            return None, None
