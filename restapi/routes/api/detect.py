from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    image = await file.read()
    return JSONResponse(content={"objects": ["person", "car"]})
