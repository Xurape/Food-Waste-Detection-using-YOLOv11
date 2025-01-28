import torch
from PIL import Image
import io


class YOLO:
    def __init__(self, weights_path: str):
        self.model = self.load_model(weights_path)

    def load_model(self, weights_path: str):
        # Load the YOLO model with the given weights
        model = torch.hub.load("ultralytics/yolov5", "custom", path=weights_path)
        return model

    def detect_objects(self, image_bytes: bytes):
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))

        # Perform detection
        results = self.model(image)

        # Extract results
        detected_objects = results.pandas().xyxy[0].to_dict(orient="records")
        return detected_objects


# Example usage:
# detector = YOLODetector('path/to/yolov11-x-weights-v6.pt')
# with open('path/to/image.jpg', 'rb') as f:
#     image_bytes = f.read()
# detections = detector.detect_objects(image_bytes)
# print(detections)
