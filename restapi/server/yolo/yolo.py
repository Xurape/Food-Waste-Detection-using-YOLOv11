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

    # def predict(self, frame):
    #     try:
    #         print("Predicting...")
    #         with torch.no_grad():
    #             results = self.model(frame)
    #         detected_objects = []
    #         for result in results:
    #             for i, (mask, box) in enumerate(zip(result.masks.data, result.boxes)):
    #                 if box.cls.item() == 58.0:
    #                     # calculate area of the box
    #                     area = box.xyxy.tolist()[0]
    #                     area = (area[2] - area[0]) * (area[3] - area[1])
    #                 else:
    #                     area = mask.sum().item()
    #                 detected_objects.append(
    #                     {
    #                         "label": box.cls.item(),
    #                         "confidence": box.conf.item(),
    #                         "box": box.xyxy.tolist(),
    #                         "area": area,
    #                     }
    #                 )

    #         return detected_objects, results
    #     except Exception as e:
    #         print(f"Error predicting: {e}")
    #         return None, None

    def predict(self, frame):
        try:
            print("Predicting...")
            with torch.no_grad():
                results = self.model(frame)
            detected_objects = []
            for result in results:
                for i, (mask, box) in enumerate(zip(result.masks.data, result.boxes)):
                    area = mask.sum().item()  # Use segmentation mask for all objects
                    detected_objects.append(
                        {
                            "label": box.cls.item(),
                            "confidence": box.conf.item(),
                            "box": box.xyxy.tolist(),
                            "area": area,
                        }
                    )

            return detected_objects, results
        except Exception as e:
            print(f"Error predicting: {e}")
            return None, None
