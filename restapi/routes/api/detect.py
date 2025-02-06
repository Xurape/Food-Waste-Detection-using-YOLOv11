from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from server.yolo.yolo import YOLOModel
from PIL import Image
import torch
import io
import base64

router = APIRouter()
yolo_model = YOLOModel()


@router.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))
    detected_objects, results = yolo_model.predict(image)

    if results is None:
        return JSONResponse(
            content={"error": "Error in object detection"}, status_code=500
        )

    # Save temporary image with detections
    output_image_path = "output_image.jpg"
    results[0].save(output_image_path)

    # Convert image to base64
    with open(output_image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    # Calculate waste percentage
    garbage_classes = {35.0, 31.0, 42.0}

    plate_area = 0
    garbage_area = 0
    food_area = 0

    for obj in detected_objects:
        print(f"Detected object: {obj}")
        if obj["label"] == 58.0:
            plate_area += obj["area"]

        if obj["label"] in garbage_classes:
            garbage_area += obj["area"]

        if obj["label"] not in garbage_classes and obj["label"] != 58.0:
            food_area += obj["area"]

    print(f"Plate area: {plate_area}")
    print(f"Garbage area: {garbage_area}")
    print(f"Food area: {food_area}")

    if plate_area > garbage_area:
        # formula nº 1 | Results:
        # (dir 7): 64.66% | 84.82% | 47.42% | 24.36%
        # waste_percentage = ((food_area - garbage_area) / plate_area * 0.8) * 100

        # formula nº 2 | Results
        # (dir 7): 100% | 100% | 100% | 72.12%
        # conclusion: formula nº 2 has better accuracy
        waste_percentage = (food_area / (plate_area - garbage_area)) * 100
    else:
        waste_percentage = 0

    waste_percentage = 100 if waste_percentage > 100 else waste_percentage
    waste_percentage = 0 if waste_percentage < 0 else waste_percentage

    return JSONResponse(
        content={
            "objects": detected_objects,
            "image_base64": base64_image,
            "waste_percentage": waste_percentage,
        }
    )
