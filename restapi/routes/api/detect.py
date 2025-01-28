from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from server.yolo.yolo import YOLOModel
from PIL import Image
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

    # Save the image with detections
    output_image_path = "output_image.jpg"
    results[0].save(output_image_path)

    # Convert image to base64
    with open(output_image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    return JSONResponse(
        content={
            "objects": detected_objects,
            "image_base64": base64_image,
        }
    )
