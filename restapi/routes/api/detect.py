from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from server.yolo.yolo import YOLOModel
from PIL import Image
import io
import base64

router = APIRouter()
yolo_model = YOLOModel()

label_map = {
    58.0: "plate",
    63.0: "garbage",
    35.0: "knife",
    20.0: "fork",
    21.0: "cup",
}


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
    plate_area = 0
    waste_area = 0
    total_food_area = 0
    waste_classes = {"garbage", "knife", "fork", "cup"}

    for obj in detected_objects:
        numeric_label = obj["label"]
        label = label_map.get(numeric_label, "unknown")
        box = obj["box"]

        print(f"Detected object: {label} with box: {box}")

        if len(box) != 1 or len(box[0]) != 4:
            print(f"Unexpected box format: {box}")
            continue

        box = box[0]

        if label == "plate":
            plate_area = (box[2] - box[0]) * (box[3] - box[1])
            print(f"Plate area: {plate_area}")
            break

    if plate_area == 0:
        return JSONResponse(content={"error": "Plate not detected"}, status_code=400)

    for obj in detected_objects:
        numeric_label = obj["label"]
        label = label_map.get(numeric_label, "unknown")
        box = obj["box"]

        if len(box) != 1 or len(box[0]) != 4:
            print(f"Unexpected box format: {box}")
            continue

        box = box[0]

        if label in waste_classes:
            box_area = (box[2] - box[0]) * (box[3] - box[1])
            waste_area += box_area
            print(f"Waste area: {waste_area}")
        else:
            box_area = (box[2] - box[0]) * (box[3] - box[1])
            total_food_area += box_area
            print(f"Food area: {total_food_area}")

    waste_percentage = (
        (waste_area / total_food_area) * 100 if total_food_area > 0 else 0
    )

    print(f"Waste percentage: {waste_percentage}")

    return JSONResponse(
        content={
            "objects": detected_objects,
            "image_base64": base64_image,
            "waste_percentage": waste_percentage,
        }
    )
